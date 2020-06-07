from SingleTreeCrawler import SingleTreeCrawler
from anytree import RenderTree

if __name__ == "__main__":
    crawler = SingleTreeCrawler("http://www.google.com", 2 )
    web_pages_tree = crawler.get_web_pages_tree()

    #print the urls tree
    for pre, fill, node in RenderTree(web_pages_tree):
        print("%s%s" % (pre, node.url))

