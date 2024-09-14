import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from datetime import datetime
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import certifi

from data_management import create_ttl_index, lru_cache_update, manage_cloudinary_storage

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'), tlsCAFile=certifi.where())
db = client[os.getenv('MONGODB_DB')]
memes_collection = db['memes']

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def scrape_xiaohongshu_memes():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    url = 'https://www.xiaohongshu.com/search_result?keyword=meme'
    driver.get(url)
    
    # Wait for the content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "note-item"))
    )
    
    # Scroll to load more content
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    meme_posts = soup.find_all('div', class_='note-item')

    for post in meme_posts[:50]:  # Limit to 50 posts
        title = post.find('div', class_='title').text.strip()
        image_url = post.find('img')['src']
        post_time = post.find('div', class_='time').text.strip()

        # Check if the post has #meme hashtag
        hashtags = post.find_all('span', class_='hashtag')
        if any('#meme' in tag.text for tag in hashtags):
            # Check if meme already exists in database
            existing_meme = memes_collection.find_one({'originalUrl': image_url})
            if not existing_meme:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(image_url)

                # Save meme data to MongoDB
                meme_data = {
                    'title': title,
                    'imageUrl': upload_result['secure_url'],
                    'source': 'Xiaohongshu',
                    'originalUrl': image_url,
                    'postTime': post_time,
                    'createdAt': datetime.utcnow()
                }
                memes_collection.insert_one(meme_data)
    lru_cache_update()
    manage_cloudinary_storage()
    driver.quit()

if __name__ == '__main__':
    create_ttl_index()
    scrape_xiaohongshu_memes()