import unittest

import csvhound.core
import agate
from agate import AgateTestCase

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

    # def test_describe_table(self):
        # self.rows = (
            # (1, 'a', True, '11/4/2015', '11/4/2015 12:22 PM', '4:15'),
            # (2, u'👍', False, '11/5/2015', '11/4/2015 12:45 PM', '6:18'),
            # (None, 'b', None, None, None, None)
        # )

        # self.column_names = [
            # 'number', 'text', 'boolean', 'date', 'datetime', 'timedelta'
        # ]

        # self.column_types = [
            # Number(), Text(), Boolean(), Date(), DateTime(), TimeDelta()
        # ]
        # model = csvhound.core.BaseHound()
        # table = model.get_table_from_file('test.csv')
        # # should return an iterable of columns and column types
        # description = model.describe_table()
        # zipped = zip(self.column_names, self.column_types)


# class TestStringMethods(unittest.TestCase):

    # def test_upper(self):
        # self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())

    # def test_split(self):
        # s = 'hello world'
        # self.assertEqual(s.split(), ['hello', 'world'])
        # # check that s.split fails when the separator is not a string
        # with self.assertRaises(TypeError):
            # s.split(2)

if __name__ == '__main__':
    unittest.main()
