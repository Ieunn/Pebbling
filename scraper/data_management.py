from pymongo import MongoClient, DESCENDING
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB')]
memes_collection = db['memes']

MAX_DOCS = 1000  # Maximum document
DURATION = 7*24*60*60
MEME_SCORE_THRESHOLD = 10

def create_ttl_index():
    memes_collection.create_index("createdAt", expireAfterSeconds=DURATION)  # Expire in 7 days

def lru_cache_update():
    # Get total number of documents
    total_docs = memes_collection.count_documents({})
    
    if total_docs > MAX_DOCS:
        # Find the oldest documents
        oldest_docs = memes_collection.find().sort("createdAt", 1).limit(total_docs - MAX_DOCS)
        
        # Delete these documents
        for doc in oldest_docs:
            memes_collection.delete_one({"_id": doc["_id"]})

def clean_low_score_memes():
    # Delete memes score below some value
    memes_collection.delete_many({"score": {"$lt": MEME_SCORE_THRESHOLD}})

def manage_cloudinary_storage():
    # TODO: Add manager cloudinary storage logic, for example, delete pictures that no longer referenced in MongoDB
    pass