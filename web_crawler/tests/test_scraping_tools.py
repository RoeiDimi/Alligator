import os
import sys
import unittest
from unittest.mock import patch, Mock

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from scraping_tools import extract_links

class TestScrapingTools(unittest.TestCase):

    def test_extract_links_ok(self):
        test_html = '''<html> random text
                            <a href="www.link1.com">link text</a>
                            <a href="https://link2.co.il">link text</a>

                            randommmmm
                            <a href="http://link3.net/randomPage.php?getParam1=3&getParam2=7">link text</a>
                            <a href="/relativeLink.asp">link text</a>

                            some more random test
                        </html>'''

        base_url = "http://www.baseUrl.com"

        # Note: The implementation of extract_links seems to force "http://" if scheme is missing.
        # "www.link1.com" -> "http://www.link1.com"
        # "/relativeLink.asp" -> "http://www.baseUrl.com/relativeLink.asp"

        links = set(['http://www.link1.com', 'https://link2.co.il',
                     'http://link3.net/randomPage.php?getParam1=3&getParam2=7',
                     base_url + '/' + 'relativeLink.asp'])

        # NOTE: The current implementation logic regarding relative paths in scraping_tools.py might produce double slashes or missing slashes depending on input.
        # Let's adjust expected set if needed or fix logic.
        # urlparse("/relativeLink.asp").path is "/relativeLink.asp"
        # base + urlparse(link).path -> "http://www.baseUrl.com" + "/relativeLink.asp" -> "http://www.baseUrl.com/relativeLink.asp"

        extracted = extract_links(base_url, test_html)

        # The original test expected exact matches.
        # We need to verify what the actual function returns because the original test was using exact string matching but the function modifies links.

        # Wait, the original test code I read had:
        # links = set(['http://www.link1.com', ...])
        # So I will preserve the original test logic but wrapped in a class.

        self.assertEqual(links, extracted)

if __name__ == '__main__':
    unittest.main()
