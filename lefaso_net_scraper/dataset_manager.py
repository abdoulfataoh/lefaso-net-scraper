# coding: utf-8

import logging
import json
from typing import Any
from typing import List
from typing import Literal
from pathlib import Path

logger = logging.getLogger(__name__)

class DatasetManager():

    _dataset: Any
    _dataset_type: str
    _dataset_path: Path
    _cache_size: int
    _cache_count: int = 0

    def __init__(
            self,
            dataset_type: Literal['json_list', 'csv'],
            dataset_path: Path,
            cache_size: int = 32
    ):
        self._dataset_type = dataset_type
        self._dataset_path = dataset_path
        self._cache_size = cache_size
        self._cache = []

        if self._dataset_type == 'json_list':
            try:
                with open(dataset_path, 'r') as file:
                    self._dataset = json.load(file)
            except FileNotFoundError:
                logger.warning(f'We can not found dataset from {dataset_path}')
                logger.info(f'We will create new dataset at {dataset_path}')
                self._dataset = []
            except json.decoder.JSONDecodeError:
                logger.warning('The dataset is empty')
                
                


        elif self._dataset_type == 'csv':
            raise Exception('This feature is currently not implemented')

    def append(self, data: Any) -> bool:
        self._dataset.append(data)
        self._cache_count = self._cache_count + 1
        if self._cache_count >= self._cache_size:
            self.save()
            self._cache_count = 0
            return True
        return False

    def save(self) -> bool:
        if self._dataset_type == 'json_list':
            with open(self._dataset_path, 'w') as file:
                json.dump(self._dataset, file, indent=2, ensure_ascii=False)
                # logger.info('-------SAVE DATASET-------')
                return True
        return False
