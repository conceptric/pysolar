import unittest
import os
from pygoes.xray.data import GoesFile

class TestGoesFile(unittest.TestCase):
    """ Test the class that imports GOES-15 X-Ray data files """

    def setUp(self):
        test_root = os.path.dirname(__file__)
        test_data = os.path.join(test_root, '20130227_Gp_xr_5m.txt')
        self.goesfile = GoesFile(test_data)

    def test_requires_path(self):
        with self.assertRaises(Exception):
            GoesFile()

    def test_exists(self):
        self.assert_(self.goesfile)

    def test_length(self):
        expected = 288
        actual = len(self.goesfile.table)
        self.assertEqual(actual, expected)

    def test_original_columns(self):
        expected = ['col1', 'col2', 'col3', 'col4', 'col7', 'col8']
        actual = sorted(self.goesfile.columns.keys())
        self.assertEqual(actual, expected)
        
    def test_new_columns(self):
        expected = ('year', 
                    'month',
                    'day',
                    'time',
                    'datetime',
                    '0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)')
        actual = self.goesfile.table.names
        self.assertEqual(actual, expected)

    def test_first_datetime(self):
        expected = "2013-02-27 00:00"
        actual = self.goesfile.table.datetime[0]
        self.assertEqual(actual, expected)
        
    def test_last_datetime(self):
        expected = "2013-02-27 23:55"
        actual = self.goesfile.table.datetime[287]
        self.assertEqual(actual, expected)        