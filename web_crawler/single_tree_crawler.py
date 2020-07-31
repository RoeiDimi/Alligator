from exceptions import TooManyTriesException
from web_crawler import WebCrawler
from web_page_info_node import WebPageInfoNode
from scraping_tools import extract_html_and_headers, extract_links
import asyncio


class SingleTreeCrawler(WebCrawler):
    """
    Scrapes the subtree of web pages starting from starting_url, up to max_depth depth
    follows the links in every web page and returns a tree containing the html of the pages

    uses asyncio for asynchronous tasks
    """

    def __init__(self, starting_url, max_depth, session, semaphore):
        super(SingleTreeCrawler, self).__init__()

        self.session = session
        self.semaphore = semaphore

        self.head = None
        self.current_level_links = None

        self.starting_url = starting_url
        self.max_depth = max_depth
        self.visited = set(starting_url)
        self.current_depth = 1

    async def get_web_pages_tree(self):
        if self.head is None:
            first_lvl_html_headers_tuple = await extract_html_and_headers(self.starting_url, self.session,
                                                                          self.semaphore)
            if first_lvl_html_headers_tuple is None:
                return None
            first_lvl_html = first_lvl_html_headers_tuple[0]
            self.head = await create_web_page_node(self.starting_url, None, self.session, self.semaphore)
            if self.head is None:
                print("couldnt get {0}".format(self.starting_url))
                return None
            self.current_level_links = extract_links(self.starting_url, first_lvl_html)

        await self.__create_subtree_recursive(self.head, self.current_depth)
        print("tree {0} finished".format(self.starting_url))
        return self.head

    async def __create_subtree_recursive(self, current_web_node, current_depth):
        children_futures = []

        if current_depth < self.max_depth:
            for link in current_web_node.get_links():
                if link not in self.visited:
                    # Get all the futures so we dont block on network requests
                    current_future = asyncio.create_task(
                        create_web_page_node(link, current_web_node, self.session, self.semaphore))
                    children_futures.append(current_future)
            current_depth = current_depth + 1

            # Wait for all the current level requests to perform asynchrounosly
            children_nodes = await asyncio.gather(*children_futures)

            successful_children_nodes = []
            for new_node in children_nodes:
                if new_node is not None:
                    self.visited.add(new_node.get_url())
                    successful_children_nodes.append(new_node)

            # asynchrounosly call the recursion on all children nodes
            children_rec_calls = asyncio.gather(
                *[self.__create_subtree_recursive(child, current_depth) for child in successful_children_nodes])
            await children_rec_calls


async def create_web_page_node(url, parent, session, semaphore):
    try:
        html_headers_tuple = await extract_html_and_headers(url, session, semaphore)

        if html_headers_tuple is not None:
            links = extract_links(url, html_headers_tuple[0])
            return WebPageInfoNode(url, html_headers_tuple[0], html_headers_tuple[1], links, parent)
        return None
    except Exception as e:
        print("Exception in create_web_page: {0}".format(str(e)))
