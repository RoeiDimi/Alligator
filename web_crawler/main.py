from single_tree_crawler import SingleTreeCrawler
from anytree import RenderTree

if __name__ == "__main__":

    google_tree = SingleTreeCrawler("http://www.google.com", 2).get_web_pages_forrest()[0]
    ynet_tree = SingleTreeCrawler("http://www.ynet.co.il", 1).get_web_pages_forrest()[0]
    crawled_forrest = [google_tree, ynet_tree]

    for tree in crawled_forrest:
        #print the urls tree
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.url))