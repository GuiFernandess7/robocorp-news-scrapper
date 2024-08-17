from robocorp.tasks import task
from scraper import NewsScraper
import time

@task
def minimal_task():
    url = "https://www.aljazeera.com/"
    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url(url)
    time.sleep(3.0)
    scraper.driver_quit()