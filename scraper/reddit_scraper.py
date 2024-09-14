import praw
import requests
import os
from pymongo import MongoClient
from dotenv import load_load_dotenv

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
            # Upload image to Cloudinary
            upload_result = cloudinary.uploader.upload(post.url)
            
            # Save meme data to MongoDB
            meme_data = {
                'title': post.title,
                'imageUrl': upload_result['secure_url'],
                'source': 'Reddit',
                'originalUrl': post.url,
                'createdAt': datetime.utcnow()
            }
            memes_collection.insert_one(meme_data)

if __name__ == '__main__':
    scrape_reddit_memes()