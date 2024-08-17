from robocorp.tasks import task
from robocorp.tasks import task
from scraper import NewsScraper
from robocorp import workitems

@task
def minimal_task():
    scraper = NewsScraper()
    scraper.open_browser("https://www.reuters.com")
    scraper.close_browser()