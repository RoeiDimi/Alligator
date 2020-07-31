"""
this module implements functions that help store crawling data in different databases
"""

import asyncio
from DAL import elastic_search


def handle(pages_forrest):
    """
    store a forrest of web pages
    """
    asyncio.run(create_tree_futures(pages_forrest))


async def create_tree_futures(pages_forrest):
    tree_futures = [asyncio.create_task(handle_tree(tree)) for tree in pages_forrest]
    return await asyncio.gather(*tree_futures)


async def handle_tree(head):
    """
    store a tree of web pages
    """
    current_node_future = asyncio.create_task(handle_page(head))
    children_futures = [asyncio.create_task(handle_tree(child)) for child in head.children]

    await asyncio.gather(*children_futures, current_node_future)


async def handle_page(web_page_info):
    """
    store a single web page
    """
    elastic_search.insert_web_page(web_page_info)
