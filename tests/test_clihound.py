import unittest

import csvhound.core
import agate
from agate import AgateTestCase
from agate.data_types import *

class HoundTestCase(AgateTestCase):
    def test_model_creation(self):
        """Does initializing CSVHound object work?"""
        model = csvhound.core.BaseHound()
        self.assertIsInstance(model, csvhound.core.BaseHound)

    def test_get_table_from_file(self):
        """Does the table object created by CSVHound equal one created by Agate?"""
        model = csvhound.core.BaseHound()
        table_agate = agate.Table.from_csv('test.csv')
        table_hound = model.get_table_from_file('test.csv')

        self.assertColumnNames(table_hound, table_agate.column_names)
        self.assertColumnTypes(table_hound, [type(c) for c in table_agate.column_types])

        self.assertRows(table_hound, table_agate.rows)

    def test_describe_table(self):
        self.rows = (
            (1, 'a', True, '11/4/2015', '11/4/2015 12:22 PM', '4:15'),
            (2, u'👍', False, '11/5/2015', '11/4/2015 12:45 PM', '6:18'),
            (None, 'b', None, None, None, None)
        )

        self.column_names = [
            'number', 'text', 'boolean', 'date', 'datetime', 'timedelta'
        ]

        self.column_types = [
            Number().__class__.__name__, 
            Text().__class__.__name__, 
            Boolean().__class__.__name__, 
            Date().__class__.__name__, 
            DateTime().__class__.__name__, 
            TimeDelta().__class__.__name__
        ]
        model = csvhound.core.BaseHound()
        table = model.get_table_from_file('test.csv')
        description = model.describe_table()
        zipped = zip(self.column_names, self.column_types)

        self.assertListEqual(list(description), list(zipped))

    def test_distinct_values(self):
        column_names: List = [
            'id',
            'name', 
            'dob',
            'last seen',
            'size', 
            'active',
            ]
        column_types: List = [
                agate.Number(),
                agate.Text(), 
                agate.Date(),
                agate.DateTime(),
                agate.Text(), 
                agate.Boolean(),
                ]

        rows = [
                (1, 'Alvin Cotton', '03-01-1980', '06-30-2019 12:12:00','L', True),
                (2, 'Usmaan Rojas', '01-12-1978', '06-30-2019 12:12:00','S', False),
                (3, 'Kingston Odling', '04-09-1990', '06-30-2019 12:12:00','M', True),
                (3, 'Pooja Gillespie', '10-07-1985', '06-30-2019 12:12:00','S', True),
                (4, 'Hal Blake', '08-17-1989', '06-30-2019 12:12:00','L', True),
                (5, 'Shannen Blevins', '06-10-1981', '06-30-2019 12:12:00','M', False),
                (5, 'Courteney Weston', '04-23-1992', '06-30-2019 12:12:00','M', False),
                (6, 'Conner Calhoun', '05-16-1977', '06-30-2019 12:12:00','XL', True),
                (7, 'Susie Rasmussen', '02-08-1987', '06-30-2019 12:12:00','L', False),
                (8, 'Cassie Beltran', '12-15-1982', '06-30-2019 12:12:00','M', True)
            ]

        model = csvhound.core.BaseHound()
        table = model.get_table_from_file('sample-data/test-distinct.csv')
        distinct = model.distinct_values('size')
        agate_table = agate.Table(rows, column_names, column_types)
        distinct_agate = agate_table.select('size').distinct('size')

        # now do the testing
        self.assertColumnNames(distinct, ('size',))
        self.assertColumnTypes(distinct, [type(c) for c in distinct.column_types])
        self.assertRows(distinct, distinct_agate)

if __name__ == '__main__':
    unittest.main()
