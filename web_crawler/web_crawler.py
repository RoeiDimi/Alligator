from abc import ABC, abstractmethod

class WebCrawler(ABC):

    '''
    A base class for crawlers

    a crawler is expected to implement def get_web_pages_tree and returns a forrest
    a forrest is a list of trees created by anytree module
    a tree should contain a starting page that started a crawl as the head where children of a node are
    the pages accessible from the page according to the crawler's crawling policy

    '''
    def __init__(self):
        super.__init__()

    @abstractmethod
    def get_web_pages_forrest(self):
        pass