import tweepy
import json
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Twitter API credentials
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# Twitter accounts to monitor
TWITTER_ACCOUNTS = [
    'ETMarkets',
    'Breakoutrade94',
    'Trading4Bucks'
]

class TwitterParser:
    def __init__(self):
        # Initialize API client
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
    def get_user_ids(self):
        """Get Twitter user IDs for the accounts we want to monitor"""
        user_ids = []
        for username in TWITTER_ACCOUNTS:
            try:
                user = self.client.get_user(username=username)
                if user.data:
                    user_ids.append(user.data.id)
            except Exception as e:
                print(f"Error getting user ID for {username}: {str(e)}")
        return user_ids

    def format_tweet_data(self, tweet, author):
        """Format tweet data according to the required structure"""
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist)
        
        return {
            "id": tweet.id,
            "created_at": current_time.isoformat(),
            "updated_at": current_time.isoformat(),
            "reference_id": str(uuid.uuid4()),
            "title": tweet.text[:100] if len(tweet.text) > 100 else tweet.text,
            "author": author,
            "url": f"https://twitter.com/{author}/status/{tweet.id}",
            "hostname": "twitter.com",
            "description": tweet.text,
            "crawled_at": current_time.isoformat(),
            "published_at": tweet.created_at.isoformat() if tweet.created_at else current_time.isoformat(),
            "categories": "Markets",
            "stocks": [],
            "classes": [],
            "indices": [],
            "stock_names": [],
            "summary": None,
            "companies": [],
            "sentiment": None
        }

    def get_latest_tweets(self):
        """Get latest tweets from monitored accounts"""
        user_ids = self.get_user_ids()
        
        for user_id in user_ids:
            try:
                # Get user's information
                user = self.client.get_user(id=user_id)
                if not user.data:
                    continue
                
                # Get user's tweets
                tweets = self.client.get_users_tweets(
                    id=user_id,
                    max_results=10,
                    tweet_fields=['created_at', 'text']
                )
                
                if not tweets.data:
                    continue
                
                for tweet in tweets.data:
                    tweet_data = self.format_tweet_data(tweet, user.data.username)
                    
                    # Save tweet data to file
                    filename = f"tweets/{user.data.username}_{tweet.id}.json"
                    os.makedirs('tweets', exist_ok=True)
                    
                    with open(filename, 'w') as f:
                        json.dump(tweet_data, f, indent=4)
                    
                    print(f"Saved tweet from {user.data.username}")
                    
            except Exception as e:
                print(f"Error processing tweets for user {user_id}: {str(e)}")

def main():
    parser = TwitterParser()
    parser.get_latest_tweets()

if __name__ == "__main__":
    main()
