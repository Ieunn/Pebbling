from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
from io import BytesIO
import random
from base_scraper import BaseScraper

class XiaohongshuScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.chrome_options = Options()
        self.chrome_options.add_argument(f"user-agent={self.get_random_user_agent()}")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        self.driver.set_page_load_timeout(30)
    
    def scrape(self):
        url = 'https://www.xiaohongshu.com/search_result?keyword=meme'
        try:
            self.start_driver()
            self.driver.get(url)
            self.random_delay(5, 10)
            
            # Wait for loading
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".note-item, .note-card"))
                )
            except TimeoutException:
                print("Page load timeout, trying to proceed anyway")
            
            # Scroll to load with random pauses
            for _ in range(random.randint(5, 8)):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(1, 3)

            meme_posts = self.driver.find_elements(By.CSS_SELECTOR, ".note-item, .note-card")

            for post in meme_posts[:50]:
                try:
                    title = post.find_element(By.CSS_SELECTOR, ".title, .content-title").text.strip()
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

                except (NoSuchElementException, Exception) as e:
                    print(f"Error processing post: {e}")

        except Exception as e:
            print(f"Error during scraping: {e}")

        finally:
            if self.driver:
                self.driver.quit()
            self.manage_storage()

    def random_delay(self, min_seconds, max_seconds):
        time.sleep(random.uniform(min_seconds, max_seconds))

if __name__ == '__main__':
    scraper = XiaohongshuScraper()
    scraper.scrape()