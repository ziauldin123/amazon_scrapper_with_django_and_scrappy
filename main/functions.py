


from main.models import ScrapyItem
from scrapper import *


def crawl():
    try:
        amazon = Scraper()
        amazon.search("huggies")
    except Exception as e:
        print(e)