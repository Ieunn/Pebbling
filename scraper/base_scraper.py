import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from storage import StorageProvider
import hashlib
import certifi

class BaseScraper:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'), tlsCAFile=certifi.where())
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.memes_collection = self.db['memes']
        self.storage = StorageProvider()
        self.max_storage = 5 * 1024 * 1024 * 1024  # 5GB
        self.meme_retention_days = 30

    def hash_image(self, image_data):
        return hashlib.md5(image_data).hexdigest()

    def is_duplicate(self, image_hash):
        return self.memes_collection.find_one({'image_hash': image_hash}) is not None

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