import time
from web_crawler import crawl
from web_page_data_handlers import handle_data

SPORT_SITES = ["https://www.nbcsports.com/", "https://www.espn.com/", "https://sports.yahoo.com/", "https://www.bleacherreport.com/"]
NEWS_SITES = ["https://news.yahoo.com/", "https://www.huffpost.com/", "https://edition.cnn.com/", "https://www.nytimes.com/"]
ECOMMERCE_SITES = ["https://www.ebay.com/", "https://www.rakuten.com/", "https://www.aliexpress.com/"]
BUSINESS_SITES = ["https://www.google.com/", "https://www.microsoft.com/en-us/", "https://www.apple.com/"]
MAX_DEPTH = 3

if __name__ == '__main__':
    start = time.time()

    forrest = crawl.crawl([*SPORT_SITES, *NEWS_SITES, *ECOMMERCE_SITES, *BUSINESS_SITES], MAX_DEPTH)

    print("crawl finished in {0} seconds".format(time.time() - start))

    handle_data.handle(filter(lambda tree: tree is not None, forrest))

    print("crawl stored in ElasticSearch")
    end = time.time()
    print(end - start)
