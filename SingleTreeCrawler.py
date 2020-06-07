import requests
import re
from urllib.parse import urlparse
from WebPageInfoNode import WebPageInfoNode


class SingleTreeCrawler:
    """
    Scrapes the subtree of web pages starting from starting_url, up to max_depth depth
    follows the links in every web page and returns a tree containing the html of the pages
    """

    def __init__(self, starting_url, max_depth):
        self.max_depth = max_depth
        self.current_level_links = self.__extract_links(starting_url)
        self.head = self.__create_web_page_node(starting_url)
        self.visited = set(starting_url)
        self.current_depth = 1

    def get_web_pages_tree(self):
        self.__create_subtree_recursive(self.head, self.current_depth)
        return self.head

    def __create_subtree_recursive(self, current_web_node, current_depth):
        children_nodes = []

        if current_depth < self.max_depth:
            for link in current_web_node.get_links():
                if link not in self.visited:
                    children_nodes.append(self.__create_web_page_node(link, parent=current_web_node))
                    self.visited.add(link)
            current_depth = current_depth + 1

            for child in children_nodes:
                self.__create_subtree_recursive(child, current_depth)

    def __create_web_page_node(self, url, parent=None, children=None):
        return WebPageInfoNode(url, self.__extract_html(url), self.__extract_links(url), parent, children)

    def __extract_html(self, url):
        html = requests.get(url)
        return html.content.decode('latin-1')

    def __extract_links(self, url):
        html = self.__extract_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))