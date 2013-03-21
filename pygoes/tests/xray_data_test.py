import unittest
import os
from atpy.basetable import Table
from pygoes.xray.data import *

TEST_ROOT = os.path.dirname(__file__)
FILENAMES =  ['20130227_Gp_xr_5m.txt', '20130228_Gp_xr_5m.txt']

class TestGoesDataSet(unittest.TestCase):
    """ 
    Test the class to work with multiple 
    GOES-15 X-Ray data files 
    """
    
    def setUp(self):
        self.dataset = GoesDataSet()
            
    def test_exists(self):
        self.assert_(self.dataset)

    def test_has_empty_datafiles_attribute(self):
        self.assertEquals(self.dataset.datafiles, [])
        
    def test_add_file_to_dataset(self):
        self.dataset.compile(TEST_ROOT, [FILENAMES[0]])
        actual = len(self.dataset.datafiles)
        self.assertEquals(1, actual)

    def test_add_two_files_to_dataset(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = len(self.dataset.datafiles)
        self.assertEquals(2, actual)

class TestDataSetDateSorting(unittest.TestCase):
    """ 
    Test the methods for working with date ranges
    that spread over multiple files.
    """
    
    def setUp(self):
        self.dataset = GoesDataSet()
        self.start   = "2013-02-27 23:50"
        self.end     = "2013-02-28 00:10"
        self.records = 5
    
    def test_returns_a_table(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertIsInstance(actual, Table)

    def test_correct_number_of_records(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(len(actual), self.records)
    
    def test_files_in_date_order(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)

    def test_files_not_in_date_order(self):
        self.dataset.compile(TEST_ROOT, reversed(FILENAMES))
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)


class TestGoesFile(unittest.TestCase):
    """ 
    Test the class that imports GOES-15 X-Ray data files 
    """

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
        expected = ['col1', 'col2', 'col3', 
            'col4', 'col5', 'col6', 'col7', 'col8']
        actual = sorted(self.goesfile.columns.keys())

        self.assertEqual(actual, expected)
        
    def test_new_columns(self):
        expected = ('year', 
                    'month',
                    'day',
                    'time',
                    'JD days',
                    'JD secs',
                    '0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)',
                    'datetime',
                    'Modified JD')
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
        
    def test_get_date_range(self):
        start   = "2013-02-27 00:30"
        end     = "2013-02-27 01:00"
        actual = self.goesfile.get_date_range(start, end)

        self.assertIsInstance(actual, Table)
        self.assertEqual(actual.datetime[0], start)
        self.assertEqual(len(actual), 7)
        self.assertEqual(actual.datetime[6], end)

    def test_first_modified_jd(self):
        actual = self.goesfile.table['Modified JD'][0]
        self.assertEqual(actual, 56350.00000)
        
    def test_last_modified_jd(self):
        actual = self.goesfile.table['Modified JD'][287]
        self.assertEqual(actual, 56350.99653)
        
        
        