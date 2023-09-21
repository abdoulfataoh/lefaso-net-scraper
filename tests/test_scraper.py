# coding: utf-8

import pytest

from lefaso_net_scraper import LefasoNetScraper


@pytest.fixture
def data():
    section_url = 'https://lefaso.net/spip.php?rubrique473'
    scraper = LefasoNetScraper(section_url)
    scraper.set_pagination_range(start=20, stop=40)
    data = scraper.run()
    return data


def test_data(data):
    assert len(data) > 0
    article = data[0]
    assert article['article_topic'] != ''
    assert article['article_title'] != ''
    assert article['article_published_date'] != ''
    assert article['article_origin'] != ''
    assert article['article_url'] != ''
