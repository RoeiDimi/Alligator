from web_crawler import WebCrawler
from anytree import RenderTree

if __name__ == "__main__":

    crawler = WebCrawler([("http://www.google.com", 2), ("http://www.ynet.co.il", 1)])

    for tree in crawler.get_forrest():
        #print the urls tree
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.url))

