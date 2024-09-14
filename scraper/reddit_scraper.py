import praw
import requests
import os
from pymongo import MongoClient
from datetime import datetime
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

from data_management import create_ttl_index, lru_cache_update, clean_low_score_memes, manage_cloudinary_storage

load_dotenv()

# Reddit API credentials
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB')]
memes_collection = db['memes']

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def scrape_reddit_memes():
    subreddit = reddit.subreddit('memes')
    for post in subreddit.hot(limit=50):
        if post.url.endswith(('.jpg', '.png', '.gif')):
            # Check if meme already exists in database
            existing_meme = memes_collection.find_one({'originalUrl': post.url})
            if not existing_meme:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(post.url)
                
                # Save meme data to MongoDB
                meme_data = {
                    'title': post.title,
                    'imageUrl': upload_result['secure_url'],
                    'source': 'Reddit',
                    'originalUrl': post.url,
                    'createdAt': datetime.utcnow(),
                    'score': post.score,
                    'postTime': datetime.fromtimestamp(post.created_utc)
                }
                memes_collection.insert_one(meme_data)
    lru_cache_update()
    clean_low_score_memes()
    manage_cloudinary_storage()

if __name__ == '__main__':
    create_ttl_index()
    scrape_reddit_memes()