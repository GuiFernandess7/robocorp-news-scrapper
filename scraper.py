"""Module for scraping news from Reuters"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import logging

class NewsScraper:
    """Class for Scrapping news."""

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def set_chrome_options(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self, browser="Chrome"):
        options = self.set_chrome_options()
        if browser.lower() == "chrome":
            self.logger.warning("Using Chrome WebDriver.")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        else:
            self.logger.error("Unsupported browser. Only Chrome is supported.")
            raise ValueError("Unsupported browser")

    def __check_driver(self):
        if not self.driver:
            self.logger.error("Driver not initialized.")
            raise RuntimeError("Driver not initialized.")

    def set_page_size(self, width: int, height: int):
        self.__check_driver()
        self.driver.set_window_size(width, height)

    def open_url(self, url: str, screenshot: str = None):
        self.__check_driver()
        self.driver.get(url)
        if screenshot:
            self.driver.get_screenshot_as_file(screenshot)
            self.logger.info(f"Screenshot saved as {screenshot}")

    def count_occurrences(self, text: str, phrase: str) -> int:
        return text.lower().count(phrase.lower())

    def search(self, search_phrase: str):
        self._click_search_button()
        self._enter_search_phrase(search_phrase)

    def _click_search_button(self):
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'SearchOverlay-search-button'))
        )
        search_button.click()

    def _enter_search_phrase(self, search_phrase: str):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'SearchOverlay-search-input'))
        )
        search_input.send_keys(search_phrase)
        search_input.send_keys(Keys.RETURN)

    def get_results(self):
        results_div = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'SearchResultsModule-results'))
        )
        return results_div.find_elements(By.CLASS_NAME, 'PageList-items-item')

    def extract_item_detail(self, item, class_name: str, default: str) -> str:
        try:
            item_content = item.find_element(By.XPATH, f".//div[contains(@class, 'PagePromo')]//div[contains(@class, 'PagePromo-content')]")
            return item_content.find_element(By.XPATH, f".//div[contains(@class, '{class_name}')]").text
        except Exception as e:
            self.logger.error(f"Error finding {class_name}: {e}")
            return default

    def store_results(self, items, search_phrase: str, month: int = 0):
        if month < 0:
            raise ValueError("Invalid month.")

        current_month = datetime.now().strftime('%B')

        for item in items:
            title = self.extract_item_detail(item, 'PagePromo-title', "No title available")
            description = self.extract_item_detail(item, 'PagePromo-description', "No description available")
            date = self.extract_item_detail(item, 'PagePromo-byline', "No date available")
            title_occ = self.count_occurrences(title, phrase=search_phrase)
            description_occ = self.count_occurrences(description, phrase=search_phrase)

            if current_month in date:
                print(title)
                print(description)
                print(date)
                print(title_occ)
                print(description_occ)
                print("---------------------------------")

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver quit successfully.")