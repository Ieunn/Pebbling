from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
from io import BytesIO
import os
from base_scraper import BaseScraper

class XiaohongshuScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        url = 'https://www.xiaohongshu.com/search_result?keyword=meme'
        self.driver.get(url)
        
        # Waiting for loading
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "note-item"))
        )

        # Scroll to load more
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        meme_posts = self.driver.find_elements(By.CLASS_NAME, "note-item")

        for post in meme_posts[:50]:
            try:
                title = post.find_element(By.CLASS_NAME, "title").text.strip()
                image = post.find_element(By.TAG_NAME, "img")
                image_url = image.get_attribute("src")
                
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    file_obj = BytesIO(image_data)
                    object_name = f"xiaohongshu_{int(time.time())}_{title[:20]}.jpg"
                    uploaded_url = self.storage.upload_fileobj(file_obj, object_name)
                    
                    if uploaded_url and self.save_meme(title, uploaded_url, 'Xiaohongshu', image_url, image_data):
                        print(f"Saved new meme: {title}")
            except Exception as e:
                print(f"Error processing post: {e}")

        self.driver.quit()
        self.manage_storage()

if __name__ == '__main__':
    scraper = XiaohongshuScraper()
    scraper.scrape()