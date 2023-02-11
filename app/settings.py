# coding: utf-8


import logging

from environs import Env


env = Env()

# [GENRAL Config]
logging.basicConfig(level=logging.INFO)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# [PATH Config]

ASSETS_PATH = env.path('ASSETS_PATH', r'assets')
DATASET_PATH = env.path('DATASET_PATH', ASSETS_PATH / 'dataset' / 'lefaso.json')

# [LEFASO.NET Config]
LEFASO_SITE_URL = env.str('LEFASO_SITE_URL','https://lefaso.net')
LEFASO_PAGING_STEP = env.int('LEFASO_PAGING_STEP', 20)
LEFASO_START_PAGE = env.int('LEFASO_START_PAGE', 0)
LEFASO_END_PAGE = env.int('LEFASO_END_PAGE', 10_000)
LEFASO_DATE_FORMAT = env.str('LEFASO_DATE_FORMAT', '%Y-%m-%dT%H:%M:%SZ')
LEFASO_TOPICS = env.list(
    'LEFASO_TOPICS',
    [
    
        {'topic_path': 'spip.php?rubrique473&debut_articles={page}#pagination_articles', 'start_page': 0, 'end_page': 40},


    ]

)
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique2', 'start_page': 0, 'end_page': 12140}, politique ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique4', 'start_page': 0, 'end_page': 32480}, societe ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique3', 'start_page': 0, 'end_page': 7100}, economie ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique62', 'start_page': 0, 'end_page': 4460},  Diplomatie - Coopération ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique18', 'start_page': 0, 'end_page': 4120}, culture ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique8', 'start_page': 0, 'end_page': 580}, portrait ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique6', 'start_page': 0, 'end_page': 4600}, Multimédia ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique5', 'start_page': 0, 'end_page': 5800}, sport ok
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique7', 'start_page': 0, 'end_page': 7240}, ..
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique13', 'start_page': 0, 'end_page': 1060}, ong, cooperation
        # {'topic_path': 'https://www.lefaso.net/spip.php?rubrique473', 'start_page': 0, 'end_page': 40}, ...
