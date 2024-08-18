from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
from scraper import NewsScraper

import os
import logging

@task
def run_news_task():
    url = os.getenv('URL', 'https://apnews.com/')
    search_phrase = os.getenv('search_phrase', "Artificial Intelligence")

    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url(url)

    scraper.search(search_phrase)
    results = scraper.get_results()
    scraper.store_results(results, search_phrase)

    scraper.driver_quit()

if __name__=="__main__":
    run_news_task()

    """
    library = WorkItems()
        library.get_input_work_item()

        variables = library.get_work_item_variables()
        for variable, value in variables.items():
            print("%s = %s", variable, value)
    """