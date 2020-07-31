from single_tree_crawler import SingleTreeCrawler
import asyncio
import aiohttp


def crawl(sites_list, max_depth):
    return asyncio.run(__main(sites_list, max_depth))


async def __main(sites_list, max_depth):
    try:
        semaphore = asyncio.Semaphore(40)
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=40))
        crawled_forrest = [SingleTreeCrawler(site, max_depth, session, semaphore).get_web_pages_tree()
                           for site in sites_list]
        crawled_forrest = await asyncio.gather(*crawled_forrest)
        return crawled_forrest
    except Exception:
        print("Unexpected exception on __main in crawl.py")
    finally:
        await session.close()

