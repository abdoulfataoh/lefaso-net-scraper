# # coding: utf-8

# from app import lefaso_scaper_jobs

# for job in lefaso_scaper_jobs:
#     job.run()

from app import lefaso_scraper_patch
import asyncio
import pandas as pd




sheets_names = [
    'Politique',
]

async def run_path():
    for sheet_name in sheets_names:
        df = pd.read_excel(r'dataset.xlsx', sheet_name=sheet_name)
        urls = df['url']
        await lefaso_scraper_patch.run_add_paragraph(urls)


asyncio.run(run_path())
