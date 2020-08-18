"""
Elastic Search data handler
"""
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import exceptions
from web_crawler.web_page_info_node import WebPageInfoNode
from urllib.parse import urlparse
import pytz
import string

HOST = "10.0.0.112"
ALL_PAGES_INDEX = "all_web_pages_small_html-index"
MAX_HTML_SIZE_CHARS = 10 ** 4


def insert_web_page(web_page_info):
    es = Elasticsearch(HOST)
    try:
        es.index(index=ALL_PAGES_INDEX, op_type='create', id=web_page_info.url[:500],
                 body=web_page_to_json(web_page_info))
    except exceptions.ConflictError:
        print("failed to add " + web_page_info.url + " because it already exists in elastic")


def web_page_to_json(web_page_info):
    parsed_uri = urlparse(web_page_info.get_url())
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    utc_dt = datetime.now(pytz.utc)
    local_dt = utc_dt.astimezone(pytz.timezone('Israel'))

    clean_web_page = prepare_for_elastic(web_page_info)

    json = {
        'timestamp': local_dt,
        'domain': domain,
        'url': clean_web_page.get_url(),
        'links': clean_web_page.get_links(),
        'html': clean_web_page.get_html(),
        'headers': clean_web_page.get_headers(),
    }

    return json


def sanitize_string(s):
    return ''.join(filter(lambda x: x in string.printable, s))


def prepare_for_elastic(web_page_info):
    links_list = []
    for item in web_page_info.links:
        links_list.append(sanitize_string(item))

    headers = {}
    for key, value in web_page_info.get_headers().items():
        headers[key] = value

    return WebPageInfoNode(sanitize_string(web_page_info.url),
                           sanitize_string(web_page_info.html[:MAX_HTML_SIZE_CHARS]), headers, links_list)
