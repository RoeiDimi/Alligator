import requests
import re
from urllib.parse import urlparse
from web_crawler import WebCrawler
from web_page_info_node import WebPageInfoNode

LINKS_BLACKLIST_WORDS = ['mailto', 'javascript', ' ']


class SingleTreeCrawler(WebCrawler):
    """
    Scrapes the subtree of web pages starting from starting_url, up to max_depth depth
    follows the links in every web page and returns a forrest with a single tree containing the html of the pages
    """

    def __init__(self, starting_url, max_depth):
        self.max_depth = max_depth
        self.current_level_links = self.__extract_links(starting_url)
        self.head = self.__create_web_page_node(starting_url)
        self.visited = set(starting_url)
        self.current_depth = 1

    def get_web_pages_forrest(self):
        self.__create_subtree_recursive(self.head, self.current_depth)
        return [self.head]

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

    def __create_web_page_node(self, url, parent=None):
        return WebPageInfoNode(url, self.__extract_html(url), self.__extract_links(url), parent)

    def __extract_html(self, url):
        try:
            html = requests.get(url)
        except requests.exceptions.ConnectionError:
            html = requests.get(url.replace("https://", "http://"))
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

        good_links = [link for link in links
                if not any(word in link for word in LINKS_BLACKLIST_WORDS)]
        return set(good_links)
