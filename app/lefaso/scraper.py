# coding: utf-8

import logging
from dataclasses import dataclass
from typing import List
from typing import Literal
from typing import Dict
from datetime import datetime
from urllib.parse import urljoin
import json

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from unidecode import unidecode

from app.dataset_manager import DatasetManager


logger = logging.getLogger(__name__)

__all__ = [
    'Article',
    'LefasoNetScraper',
]


@dataclass
class Article:
    article_type: Literal['press', 'report']
    article_title: str
    topic: str
    published_date: datetime
    origin: str
    url: str
    content: str
    comments_number: int
    comments: List[str]

    def __post_init__(self):
        ...

    @staticmethod
    def to_json(date_format: str, **kwargs) -> dict:
        data = Article(**kwargs).__dict__.copy()
        data['published_date'] = data['published_date'].strftime(date_format)
        return data


class LefasoNetScraper():

    _site_url: str
    _topic_path: str
    _paging_step = int
    _start_page: int
    _end_page: int
    _site_date_format: str
    _data_template: Article
    _dm: DatasetManager

    def __init__(
        self,
        site_url: str,
        topic_path: str,
        paging_step: int,
        start_page: int,
        end_page: int,
        site_date_format: str,
        data_template: Article,
        dataset_manager: DatasetManager,
    ):
        self._site_url = site_url
        self._topic_path = topic_path
        self._paging_step = paging_step
        self._start_page = start_page
        self._end_page = end_page
        self._site_date_format = site_date_format
        self._data_template = data_template
        self._dm = dataset_manager

    def run(self):
        asyncio.run(
            self.process(callback=self._get_article_data)
        )

    async def process(self, callback):
        paginations = range(
            self._start_page,
            self._end_page,
            self._paging_step
        )
        for pagination in paginations:
            url = urljoin(self._site_url, self._topic_path)
            url = url.format(page=pagination)
            logger.info(f"get page {url}")
            req = await self._request(url)
            articles = self._get_page_articles_list(req)
            for article in articles:
                article_title = article.get('article_title')
                article_link = article.get('article_link')
                logger.info(f"get page from {article_link}")
                try:
                    article_content = await self._request(article_link)
                except Exception as e:
                    logger.warning(f'error occured at {article_link}')
                    logger.warning(e)
                    continue
                callback(article_content, article_title, article_link)
        self._dm.save()

    async def _request(self, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                html = await r.text()
                soup = BeautifulSoup(html, features='html.parser')
        return soup

    def _get_article_data(
            self,
            soup_html: BeautifulSoup,
            article_title,
            article_url
    ):
        # article_type
        article_type = 'press'

        # origin
        origin = 'lefaso.net'

        # organization
        topic = soup_html.select('#hierarchie > a')[-1].text
        
        # pusblished date
        meta = soup_html.select('#hierarchie > abbr')[0]
        pusblished_date_str = meta.attrs.get('title')
        pusblished_date = datetime.strptime(
            pusblished_date_str,
            self._site_date_format,
        )

        # content
        sumary_content = soup_html.select(
            'div[class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]'
        )[0].select('h3')[0].text

        content = unidecode(sumary_content).strip()

        try:
            div = soup_html.findAll(
                'div',
                attrs={'class': 'col-xs-12 col-sm-12 col-md-8 col-lg-8'}
            )[0].findAll(
                'div',
                attrs={'class': 'article_content'}
            )[0].findAll('p')

            for p in div:
                content = sumary_content + '\n' + unidecode(p.text).strip()
        except Exception:
            logger.warning(f"we can't find <article_content> class from {article_url}")  # noqa: E501

        # comments
        comments_div = soup_html.select(
            '.comment-texte'
        )
        comments: List[str] = []

        for comment in comments_div:
            if comment is not None or comment != '':
                comments.append(
                    unidecode(comment.text).strip()
                )
        comments_number = len(comments)

        data = Article.to_json(
            date_format='%Y-%m-%dT%H:%M:%S',
            article_type=article_type,
            article_title=article_title,
            topic=topic,
            published_date=pusblished_date,
            origin=origin,
            url=article_url,
            content=content,
            comments_number=comments_number,
            comments=comments,
        )

        self._dm.append(data)

    def _get_page_articles_list(
        self,
        soup_html: BeautifulSoup
    ) -> List[Dict[str, str]]:
        articles = []
        article_attr = {'style': 'width:100%; height:160px;margin-top:10px; margin-bottom:10px;'}  # noqa: 501
        for article in soup_html.findAll('div', attrs=article_attr):
            content = article.select('h3 > a')[0]
            article_title = unidecode(content.text)
            article_link = urljoin(self._site_url, content.attrs.get('href'))
            articles.append(
                {
                    'article_title': article_title,
                    'article_link': article_link
                }
            )
        return articles
    
    
    async def run_add_paragraph(self, urls: List[str]):
        progess = 0
        progress_100 = len(urls)
        id = 0
        df = []

        for url in urls:
            logger.info(f'({progess}/{progress_100}) - {url}')
            progess = progess + 1
            soup = await self._request(url)

            topic = soup.select('#hierarchie > a')[-1].text

            try:
                title_div = soup.select('div[class="col-xs-12 col-sm-12 col-md-8 col-lg-8"] > h3 > p')
                for paragraph in title_div:
                    df.append(
                        {
                            'url': url,
                            'topic': topic,
                            'id': id,
                            'content': paragraph.text  
                        }
                    )
                    id = id + 1
            except Exception as e:
                logger.warning(f'{url}: {e}')

            try:
                content_div = soup.select('div[class="article_content"] > p')
                for paragraph in content_div:
                    df.append(
                        {
                            'url': url,
                            'topic': topic,
                            'id': id,
                            'content': paragraph.text  
                        }
                    )
                    id = id + 1
            except Exception as e:
                logger.warning(f'{url}: {e}')
            
        with open('df.json', 'w') as f:
            json.dump(df, f, indent=2, ensure_ascii=False)
            logger.info('-------SAVE DATASET-------')

