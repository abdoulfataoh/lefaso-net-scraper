# coding: utf-8

from app.lefaso import Article
from app.lefaso import LefasoNetScraper
from app.dataset_manager import DatasetManager
from app import settings

__all = [
    'dm',
    'lefaso_scraper_patch',
]

dm = DatasetManager(
    dataset_type='json_list',
    dataset_path=settings.DATASET_PATH,
    cache_size=1
)

lefaso_scaper_jobs = []

# for topic in settings.LEFASO_TOPICS:
#     lefaso_scaper_jobs.append(
#         LefasoNetScraper(
#             site_url=settings.LEFASO_SITE_URL,
#             topic_path=topic['topic_path'],
#             paging_step=settings.LEFASO_PAGING_STEP,
#             start_page=topic['start_page'],
#             end_page=topic['end_page'],
#             site_date_format=settings.LEFASO_DATE_FORMAT,
#             data_template=Article,
#             dataset_manager=dm,
#         )
# )



lefaso_scraper_patch = LefasoNetScraper(
    site_url=settings.LEFASO_SITE_URL,
    topic_path='',
    paging_step=0,
    start_page=0,
    end_page=0,
    site_date_format='',
    data_template=Article,
    dataset_manager=dm,
)
