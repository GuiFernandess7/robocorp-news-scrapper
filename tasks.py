from robocorp.tasks import task
from robocorp import workitems
from scraper import NewsScraper, News

URL = 'https://apnews.com/'

@task
def run_news_task():
    work_items = workitems.inputs.current.payload
    search_phrase = work_items['SEARCH_PHRASE']
    months = work_items['MONTHS']

    scraper = NewsScraper()
    scraper.set_webdriver()
    scraper.open_url(URL)

    scraper.search(search_phrase)
    results = scraper.get_results(search_phrase, month=months)
    scraper.write_to_excel(results, News, 'orders.xlsx')

    scraper.driver_quit()

if __name__=="__main__":
    run_news_task()
