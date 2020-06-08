from anytree import NodeMixin


class WebPageInfoNode(NodeMixin):
    def __init__(self, url, html, links, parent=None):
        super().__init__()

        self.parent = parent
        self.url = url
        self.html = html
        self.links = links

    def get_url(self):
        return self.url

    def get_html(self):
        return self.html

    def get_links(self):
        return self.links
