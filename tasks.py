from robocorp.tasks import task
from robocorp import workitems

from scraper import NewsScraper

@task
def minimal_task():
    url = "https://apnews.com/"
    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url(url)
    #scraper.full_page_screenshot(url)
    scraper.driver_quit()