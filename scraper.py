"""Module for scraping news from Reuters"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
from collections import namedtuple
from openpyxl import Workbook
import logging


News = namedtuple(
    "News",
    [
        "title",
        "description",
        "date",
        "pic_filename",
        "title_occurrences",
        "description_occurrences",
        "contains_money",
    ],
)


class NewsScraper:
    """Class for Scrapping news."""

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def set_chrome_options(self):
        """Chrome configuration settings"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return options

    def set_webdriver(self, browser="Chrome"):
        """Webdriver install and setup."""
        options = self.set_chrome_options()
        if browser.lower() == "chrome":
            self.logger.warning("Using Chrome WebDriver.")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        else:
            self.logger.error("Unsupported browser. Only Chrome is supported.")
            raise ValueError("Unsupported browser")

    def __check_driver(self):
        """Check if driver is enabled"""
        if not self.driver:
            self.logger.error("Driver not initialized.")
            raise RuntimeError("Driver not initialized.")

    def open_url(self, url: str):
        """Open News URL."""
        self.__check_driver()
        self.driver.get(url)

    def count_occurrences(self, text: str, phrase: str) -> int:
        """Count occurrences of text"""
        return text.lower().count(phrase.lower())

    def search(self, search_phrase: str):
        """Click and enter the search phrase in the search bar."""
        self._click_search_button()
        self._enter_search_phrase(search_phrase)

    def _click_search_button(self):
        """Find button element and execute click."""
        element = self.driver.find_element(
            By.CLASS_NAME, "SearchOverlay-search-button")
        self.driver.execute_script("arguments[0].click();", element)

    def _enter_search_phrase(self, search_phrase: str):
        """Find search bar element and send keys."""
        search_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "SearchOverlay-search-input")
            )
        )
        search_input.send_keys(search_phrase)
        search_input.send_keys(Keys.RETURN)

    def get_news_tags(self):
        """Get all news by tags."""
        results_div = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "SearchResultsModule-results")
            )
        )
        return results_div.find_elements(By.CLASS_NAME, "PageList-items-item")

    def extract_news_detail(self, item, class_name: str, default: str) -> str:
        """Extract news details based on class name."""
        try:
            item_content = item.find_element(
                By.XPATH,
                f".//div[contains(@class, 'PagePromo')]//div[contains(@class, 'PagePromo-content')]",
            )
            return item_content.find_element(
                By.XPATH, f".//div[contains(@class, '{class_name}')]"
            ).text
        except Exception as e:
            self.logger.error(f"Error finding {class_name}: {e}")
            return default

    def extract_news_picture(self, item, default=""):
        """Extract news picture address."""
        try:
            item_content = item.find_element(
                By.XPATH,
                ".//div[contains(@class, 'PagePromo')]//div[contains(@class, 'PagePromo-media')]",
            )
            img_element = item_content.find_element(
                By.XPATH,
                f".//a[contains(@class, 'Link')]//img[contains(@class, 'Image')]",
            )
            return img_element.get_attribute("src")
        except NoSuchElementException:
            return default
        except Exception as e:
            self.logger.error(f"Error finding picture: {e}")
            return default

    def get_months(self, month: int = 0):
        """Get months based on int parameter."""
        if month < 0:
            raise ValueError("Invalid month.")

        current_month = datetime.now().month

        if month == 0:
            months_to_check = [current_month]
        else:
            months_to_check = [(current_month - i) %
                               12 or 12 for i in range(month)]

        months_to_check_names = [
            datetime(2024, m, 1).strftime("%B") for m in months_to_check
        ]
        return months_to_check_names

    def contains_money(self, text):
        """Apply regex to check if money is found."""
        import re

        pattern = r"/^\$?(\d+(?:\.\d{1,2})?)$/"
        return re.search(pattern, text, re.IGNORECASE) is not None

    def get_results(self, search_phrase: str, month: int = 0):
        """Loop through news tags getting all the deatils needed."""
        months = self.get_months(month=month)
        news_tags = self.get_news_tags()
        results = []

        for news in news_tags:
            title = self.extract_news_detail(news, "PagePromo-title", " ")
            description = self.extract_news_detail(
                news, "PagePromo-description", " ")
            date = self.extract_news_detail(news, "PagePromo-byline", " ")
            picture = self.extract_news_picture(news)

            title_occ = self.count_occurrences(title, phrase=search_phrase)
            description_occ = self.count_occurrences(
                description, phrase=search_phrase)

            contains_money = self.contains_money(title) or self.contains_money(
                description
            )

            if any(month in date for month in months):
                results.append(
                    News(
                        title=title,
                        description=description,
                        date=date,
                        pic_filename=picture,
                        title_occurrences=title_occ,
                        description_occurrences=description_occ,
                        contains_money=contains_money,
                    )
                )

        return results

    @staticmethod
    def write_to_excel(results, news: News, file: str):
        """Write the results to a excel sheet."""
        wb = Workbook()
        ws = wb.active
        ws.title = "News"

        headers = news._fields
        ws.append(headers)

        for employee in results:
            ws.append(employee)

        wb.save(f"./output/{file}")

    def driver_quit(self):
        """Quit the driver."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver quit successfully.")
