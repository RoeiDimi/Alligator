import os
import sys
from unittest.mock import patch

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from scraping_tools import extract_html, extract_links


def test_extract_html_ok():
    with patch('requests.get') as mock_get:
        mock_content = "yay".encode()

        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_content

        res = extract_html("google")
        assert res == mock_content.decode('latin-1')


def test_extract_html_bad_link():
    with patch('requests.get') as mock_get:
        mock_content = "yay".encode()

        mock_get.return_value.status_code = 404
        mock_get.return_value.content = mock_content

        res = extract_html("google")
        assert res is None


def test_extract_links_ok():
    test_html = '''<html> random text 
                        <a href="www.link1.com">link text</a>
                        <a href="https://link2.co.il">link text</a>
                        
                        randommmmm
                        <a href="http://link3.net/randomPage.php?getParam1=3&getParam2=7">link text</a>
                        <a href="/relativeLink.asp">link text</a>
                        
                        some more random test
                    </html>'''

    base_url = "http://www.baseUrl.com"

    links = set(['http://www.link1.com', 'https://link2.co.il',
                 'http://link3.net/randomPage.php?getParam1=3&getParam2=7',
                 base_url + '/' + 'relativeLink.asp'])

    extracted = extract_links(base_url, test_html)
    assert links == extracted
