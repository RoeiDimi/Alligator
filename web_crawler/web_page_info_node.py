from anytree import NodeMixin


class WebPageInfoNode(NodeMixin):
    """
    encapsulates the information gathered from a crawled site
    also, its a NodeMixin which means it is a node in a tree data structure. this helps us with saving the
    data of a recursive crawl in a tree
    """
    def __init__(self, url, html, headers, links, parent=None):
        super().__init__()

        self.parent = parent
        self.url = url
        self.html = html
        self.headers = headers
        self.links = links

    def get_url(self):
        return self.url

    def get_html(self):
        return self.html

    def get_links(self):
        return self.links

    def get_headers(self):
        return self.headers
