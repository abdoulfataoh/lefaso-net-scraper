# coding: utf-8

import logging

from environs import Env


logging.basicConfig(level=logging.INFO)

env = Env()

LAFASO_URL = env.url('LAFASO_URL', 'https://lefaso.net')
LEFASO_PAGINATION_STEP = env.int('LEFASO_PAGAINATION_STEP', 20)
LEFASO_ARTICLE_ATTR = env.dict('LEFASO_ARTICLE_ATTR', {'style': 'width:100%; height:160px;margin-top:10px; margin-bottom:10px;'})
LEFASO_ARTICLE_SELECTOR = env.str('LEFASO_ARTICLE_SELECTOR', 'div.col-xs-12.col-sm-12.col-md-8.col-lg-8')
LEFASO_PAGINATION_TEMPLATE = env.str('LEFASO_PAGINATION_TEMPLATE', '&debut_articles={}#pagination_articles')

