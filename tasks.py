from robocorp.tasks import task
from scraper import NewsScraper
import time

@task
def minimal_task():
    url = "https://apnews.com/"
    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url(url)
    scraper.driver_quit()