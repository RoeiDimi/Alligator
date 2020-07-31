import pytest
import requests


def test_get_web_pages_forrest():
    test_html = '''<html> random text 
                            <a href="www.link1.com">link text</a>
                            <a href="https://link2.co.il">link text</a>

                            randommmmm
                            <a href="http://link3.net/randomPage.php?getParam1=3&getParam2=7">link text</a>
                            <a href="/relativeLink.asp">link text</a>

                            some more random test
                        </html>'''

    base_url = "http://www.baseUrl.com"
    pass
