import logging
import os
import sys
import agate

logger = logging.getLogger('csvhound')
logger.debug(__name__ + ' module loaded')

def do_another_thing():
    logger.debug('do another thing')

def file_exists(path):
    try:
        if(not os.path.exists(path)):
            raise FileNotFoundError('File not found.')
        else:
            logger.debug('File ' + path + ' exists.')
            # return True
    except FileNotFoundError as e:
        logger.warning(str(e))
        exit()
        # return False
        
class BaseHound:

    def __init__(self):
        logger.debug('BaseHound class instantiated.')
        self._table = None
        self._distinct = {}

    def get_table_from_file(self, input_file, column_types=None):
        # if file_exists(input_file):
        try:
            self._table = agate.Table.from_csv(input_file, column_types=column_types)
            logger.info('- Successfully created agate table from csv file.')
            return self._table
        except BaseException as e:
            logger.warning('- Failed to create agate table.')
            logger.warning(str(e))
            exit()

    def describe_table(self, output=sys.stdout):
        logger.debug('Describing current table.')
        self._table.print_structure(output)

    def distinct_values(self, key=None, with_count=False):
        logger.debug('distinct values for: ' + key)
        if with_count:
            table = self._table.group_by(key)
            # group_by returns a TableSet, so another step is required
            table = table.aggregate([('count',agate.Count())])
        else:
            table = self._table.select(key).distinct(key)
        
        table.print_table()

    def get_columns(self):
        columns = self._table.column_types
        print(columns[1])
