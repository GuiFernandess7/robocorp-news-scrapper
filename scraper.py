"""Module for scraping news from Reuters"""

from RPA.Browser.Selenium import Selenium
from robocorp import workitems
from selenium.webdriver import FirefoxOptions

class NewsScraper:
    def __init__(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = Selenium()

    def open_browser(self, url):
        self.browser.open_browser(url)

    def close_browser(self):
        self.browser.close_browser()

    def get_work_item(self):
        item = workitems.inputs.current
        return item

    def set_work_item(self, key, value):
        self.browser.set_variable(key, value)