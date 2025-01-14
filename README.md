# Twitter Parser

This script fetches real-time updates from specified Twitter accounts and stores them in a structured format.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the .env file is present with your Twitter API credentials.

3. Run the parser:
```bash
python twitter_parser.py
```

## Features

- Monitors tweets from specified Twitter accounts in real-time
- Stores tweet data in a structured JSON format
- Includes error handling and logging
- Supports multiple Twitter accounts

## Data Structure

The parser stores tweets in the following format:
```json
{
    "id": "tweet_id",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "reference_id": "uuid",
    "title": "tweet_text",
    "author": "username",
    "url": "tweet_url",
    "hostname": "twitter.com",
    "description": "full_tweet_text",
    "crawled_at": "timestamp",
    "published_at": "tweet_timestamp",
    "categories": "Markets",
    "stocks": [],
    "classes": [],
    "indices": [],
    "stock_names": [],
    "summary": null,
    "companies": [],
    "sentiment": null
}
```
