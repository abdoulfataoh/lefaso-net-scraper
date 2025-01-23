# coding: utf-8

import pytest

from lefaso_net_scraper import LefasoNetScraper


@pytest.fixture
def data():
    section_url = 'https://lefaso.net/spip.php?rubrique473'
    scraper = LefasoNetScraper(section_url)
    scraper.set_pagination_range(start=20, stop=60)
    data = scraper.run()
    return data


def test_data(data):
    assert len(data) > 0  # check data length
    # check sample article fields
    sample = data[0]
    assert sample['article_topic']
    assert sample['article_title']
    assert sample['article_published_date']
    assert sample['article_origin']
    assert sample['article_url']
    # check comments retrieve
    articles_comments = []
    for article in data:
        article_comments = article['article_comments']
        comments_exist = True if article_comments else False
        articles_comments.append(comments_exist)
    assert len(articles_comments) > 20
