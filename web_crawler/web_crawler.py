from single_tree_crawler import SingleTreeCrawler


class WebCrawler:

    '''
    A crawler. crawls a list of urls. receives each url with the depth which this url should be crawled into
    '''
    def __init__(self, urls_and_depths_tuples_list=None):
        self.urls_forrest = []

        if urls_and_depths_tuples_list:
            self.add_trees(urls_and_depths_tuples_list)
        pass

    def add_trees(self, urls_and_depths_tuples_list):
        for url_depth_tuple in urls_and_depths_tuples_list:
            url = url_depth_tuple[0]
            depth = url_depth_tuple[1]
            crawled_tree = SingleTreeCrawler(url, depth).get_web_pages_tree()
            self.urls_forrest.append(crawled_tree)

    def get_forrest(self):
        return self.urls_forrest