from robocorp.tasks import task
from robocorp import workitems

from scraper import NewsScraper

@task
def minimal_task():
    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url("https://www.reuters.com", screenshot="homepage.png")
    scraper.full_page_screenshot("https://www.reuters.com")
    scraper.driver_quit()