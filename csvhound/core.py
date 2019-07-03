import logging
import os
import sys
import agate

from typing import Dict, List, Iterator

logger = logging.getLogger('csvhound')
logger.debug(__name__ + ' module loaded')

def do_another_thing() -> None:
    logger.debug('do another thing')

def file_exists(path) -> bool:
    try:
        if(not os.path.exists(path)):
            raise FileNotFoundError('File not found.')
        else:
            logger.debug('File ' + path + ' exists.')
            return True
    except FileNotFoundError as e:
        logger.warning(str(e))
        # exit()
        return False
        
class BaseHound:

    def __init__(self) -> None:
        logger.debug('BaseHound class instantiated.')
        self._distinct: Dict = {}

    def get_table_from_file(self, input_file: str, column_types: List = None) -> agate.Table:
        try:
            self._table: agate.Table = agate.Table.from_csv(input_file, column_types=column_types)
            logger.info('- Successfully created agate table from csv file.')
            return self._table
        except BaseException as e:
            logger.warning('- Failed to create agate table.')
            logger.warning(str(e))
            exit()

    def describe_table(self) -> Iterator:
        logger.debug('Describing current table.')
        name_column: List = [n for n in self._table.column_names]
        type_column: List = [t.__class__.__name__ for t in self._table.column_types]
        rows: Iterator = zip(name_column, type_column)
        return rows

    def distinct_values(self, key=None, with_count=False) -> agate.Table:
        logger.debug('distinct values for: ' + key)
        if with_count:
            table = self._table.group_by(key)
            # group_by returns a TableSet, so another step is required
            table = table.aggregate([('count',agate.Count())])
        else:
            table = self._table.select(key).distinct(key)
        return table

    def get_columns(self):
        columns = self._table.column_types
        print(columns[1])
