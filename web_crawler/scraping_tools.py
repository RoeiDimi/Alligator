"""
a module that handles all the http requests and scraping
"""

import re
from urllib.parse import urlparse
import aiohttp
from aiohttp import TooManyRedirects
import contextlib

from web_crawler.exceptions import SchemalessUrlException
import async_timeout
import asyncio

from ssl import SSLError

LINKS_BLACKLIST_WORDS = ['mailto', 'javascript', ' ', 'void(0)', '{']


@contextlib.contextmanager
def suppress_ssl_exception_report():
    loop = asyncio.get_event_loop()
    old_handler = loop.get_exception_handler()
    old_handler_fn = old_handler or (lambda _loop, ctx: loop.default_exception_handler(ctx))
    def ignore_exc(_loop, ctx):
        exc = ctx.get('exception')
        if isinstance(exc, SSLError):
            return
        old_handler_fn(loop, ctx)
    loop.set_exception_handler(ignore_exc)
    try:
        yield
    finally:
        loop.set_exception_handler(old_handler)



async def fetch(url, session, semaphore):
    """
    asynchronous http get
    """
    with suppress_ssl_exception_report():
        async with semaphore:
            print("semaphore value: {0}".format(semaphore._value))
            with async_timeout.timeout(30):
                async with session.get(url, max_redirects=30) as response:
                    return await response.text('latin-1'), response.status, response.headers


async def extract_html_and_headers(url, session, semaphore):
    try:
        print("Crawl: {0}".format(url))
        response = await fetch(url, session, semaphore)
    except aiohttp.client_exceptions.ClientConnectorError:
        url = url.replace("https://", "http://")
        async with aiohttp.ClientSession() as session:
            response = await fetch(url, session, semaphore)
    except TooManyRedirects:
        # Couldnt get the html. give up
        print("Too many redirects. url: {0}".format(url))
        return None
    except asyncio.TimeoutError:
        print("Timeout. url: {0}".format(url))
        return None
    except asyncio.CancelledError:
        return None
    except Exception as e:
        print("Weird. unexpected exception in url {0}: {1}".format(url, repr(e)))
        return None

    if response[1] == 200:
        print("Success: {0}".format(url))
        return response[0], response[2]
    return None


def extract_links(url, html):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    if not parsed.scheme:
        raise SchemalessUrlException(url)

    try:
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
    except Exception:
        return []

    for i, link in enumerate(links):
        if not urlparse(link).scheme:
            link = "http://" + link
            links[i] = link

        if not urlparse(link).netloc:
            link_with_base = base + urlparse(link).path
            links[i] = link_with_base

    good_links = [link for link in links
                  if not any(word in link for word in LINKS_BLACKLIST_WORDS)]
    return set(good_links)
