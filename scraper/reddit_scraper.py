import praw
import requests
from io import BytesIO
import os
from base_scraper import BaseScraper

class RedditScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )

    def scrape(self):
        subreddit = self.reddit.subreddit('memes')
        for post in subreddit.hot(limit=50):
            if post.url.endswith(('.jpg', '.png', '.gif')):
                response = requests.get(post.url)
                if response.status_code == 200:
                    image_data = response.content
                    file_obj = BytesIO(image_data)
                    object_name = f"reddit_{post.id}{os.path.splitext(post.url)[1]}"
                    image_url = self.storage.upload_fileobj(file_obj, object_name)
                    
                    if image_url and self.save_meme(post.title, image_url, 'Reddit', post.url, image_data):
                        print(f"Saved new meme: {post.title}")

        self.manage_storage()

if __name__ == '__main__':
    scraper = RedditScraper()
    scraper.scrape()