"""
    this modules allows an easy crawl of a list of sites up to a given depth
    the user should call crawl function to do so

    the module uses asyncio in order to maximize performance by sending asynchronous http requests
"""

from web_crawler.single_tree_crawler import SingleTreeCrawler
import asyncio
import aiohttp


def crawl(sites_list, max_depth):
    """
    parameters
    ---------------
    sites_list - a list of urls to crawl
    max_depth - int. the depth of the crawl of each site (how may times should we gather html links and crawl them
                        recursively)

    returns
    ----------
    a forrest -  effectively a list of type WebPageInfoNode. each node is the head of a tree
                the tree contains the crawling results of a single url from sites_list
    """
    return asyncio.run(__main(sites_list, max_depth))


async def __main(sites_list, max_depth):
    try:
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=40))
        semaphore = asyncio.Semaphore(40)
        crawled_forrest = [SingleTreeCrawler(site, max_depth, session, semaphore).get_web_pages_tree()
                           for site in sites_list]
        crawled_forrest = await asyncio.gather(*crawled_forrest)
        return crawled_forrest
    except Exception:
        print("Unexpected exception on __main in crawl.py")
    finally:
        if session:
            await session.close()

