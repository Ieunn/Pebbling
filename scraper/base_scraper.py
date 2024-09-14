import os
import random
import requests
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from storage import StorageProvider
import hashlib
import certifi
from fake_useragent import UserAgent

class BaseScraper:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'), tlsCAFile=certifi.where())
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.memes_collection = self.db['memes']
        self.storage = StorageProvider()
        self.max_storage = 5 * 1024 * 1024 * 1024  # 5GB
        self.meme_retention_days = 30
        self.user_agent = UserAgent()
        self.proxies = [
            # TODO: Add proxy, example 'http://proxy1.example.com'
        ]

    def hash_image(self, image_data):
        return hashlib.md5(image_data).hexdigest()

    def is_duplicate(self, image_hash):
        return self.memes_collection.find_one({'image_hash': image_hash}) is not None
    
    def random_delay(self, min_delay=1, max_delay=5):
        time.sleep(random.uniform(min_delay, max_delay))
    
    def get_random_user_agent(self):
        return self.user_agent.random

    def get_random_proxy(self):
        return random.choice(self.proxies)
    
    def get_with_retry(self, url, max_retries=3):
        for _ in range(max_retries):
            try:
                headers = {'User-Agent': self.get_random_user_agent()}
                proxy = self.get_random_proxy()
                response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                self.random_delay()
        return None

    def save_meme(self, title, image_url, source, original_url, image_data):
        image_hash = self.hash_image(image_data)
        if self.is_duplicate(image_hash):
            return False

        meme_data = {
            'title': title,
            'imageUrl': image_url,
            'source': source,
            'originalUrl': original_url,
            'createdAt': datetime.utcnow(),
            'image_hash': image_hash
        }
        self.memes_collection.insert_one(meme_data)
        return True

    def manage_storage(self):
        # Delete old memes
        cutoff_date = datetime.utcnow() - timedelta(days=self.meme_retention_days)
        old_memes = self.memes_collection.find({'createdAt': {'$lt': cutoff_date}})
        for meme in old_memes:
            self.storage.delete_file(meme['imageUrl'])
            self.memes_collection.delete_one({'_id': meme['_id']})

        # LRU
        while self.get_total_storage() > self.max_storage:
            oldest_meme = self.memes_collection.find_one(sort=[('createdAt', 1)])
            if oldest_meme:
                self.storage.delete_file(oldest_meme['imageUrl'])
                self.memes_collection.delete_one({'_id': oldest_meme['_id']})
            else:
                break

    def get_total_storage(self):
        return self.storage.get_total_size()

    def scrape(self):
        raise NotImplementedError("Subclasses must implement this method")