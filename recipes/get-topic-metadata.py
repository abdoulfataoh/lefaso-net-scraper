# coding: utf-8

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

site_url = 'https://www.lefaso.net'

topics_paths = [
    '/spip.php?rubrique2',
    '/spip.php?rubrique4',
    '/spip.php?rubrique3',
    '/spip.php?rubrique62',
    '/spip.php?rubrique18',
    '/spip.php?rubrique8',
    '/spip.php?rubrique6',
    '/spip.php?rubrique5',
    '/spip.php?rubrique7',
    '/spip.php?rubrique13',                  
    '/spip.php?rubrique473',
]

for topic_path in topics_paths:
    topic_url = urljoin(site_url, topic_path)
    html = requests.get(topic_url).text
    soup = BeautifulSoup(html, features='html.parser')
    end_page = soup.select('.pagination > span > .lien_pagination')[-1]
    output = {
        'topic_path': topic_url,
        'start_page': 0,
        'end_page': end_page.text
    }

    print(f'{output},')