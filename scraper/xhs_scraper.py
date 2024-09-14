import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from datetime import datetime
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

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

def scrape_xiaohongshu_memes():
    url = 'https://www.xiaohongshu.com/explore'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    meme_posts = soup.find_all('div', class_='note-item')

    for post in meme_posts[:50]:  # Limit to 50 posts
        title = post.find('div', class_='title').text.strip()
        image_url = post.find('img')['src']

        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(image_url)

        # Save meme data to MongoDB
        meme_data = {
            'title': title,
            'imageUrl': upload_result['secure_url'],
            'source': 'Xiaohongshu',
            'originalUrl': image_url,
            'createdAt': datetime.utcnow()
        }
        memes_collection.insert_one(meme_data)

if __name__ == '__main__':
    scrape_xiaohongshu_memes()