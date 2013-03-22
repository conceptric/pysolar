import unittest
import os
from atpy.basetable import Table
from pygoes.xray.data import *

TEST_ROOT = os.path.dirname(__file__)
FILENAMES =  ['20130227_Gp_xr_5m.txt', '20130228_Gp_xr_5m.txt']

class TestDataSet(unittest.TestCase):
    """ 
    Test that the DataSet class exists and has
    the correct attributes. 
    """
    def setUp(self):
        self.dataset = GoesDataSet()
            
    def test_exists(self):
        self.assert_(self.dataset)

    def test_has_empty_datafiles_attribute(self):
        self.assertEquals(self.dataset.datafiles, [])


class TestDataSetCompile(unittest.TestCase):
    """ 
    Test that the DataSet class can import multiple 
    GOES-15 X-Ray data files.
    """
    def setUp(self):
        self.dataset = GoesDataSet()

    def test_ignores_empty_file_list(self):
        self.dataset.compile(TEST_ROOT, [])
        self.assertEquals(0, len(self.dataset.datafiles))
        
    def test_ignores_incorrect_filename_in_list(self):
        self.dataset.compile(TEST_ROOT, ['wrong_name.txt'])
        self.assertEquals(0, len(self.dataset.datafiles))        
        
    def test_add_file_to_dataset(self):
        self.dataset.compile(TEST_ROOT, [FILENAMES[0]])
        actual = len(self.dataset.datafiles)
        self.assertEquals(1, actual)

    def test_add_two_files_to_dataset(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = len(self.dataset.datafiles)
        self.assertEquals(2, actual)


class TestDataSetGetDateRanges(unittest.TestCase):
    """ 
    Test the methods for working with date ranges
    that spread over multiple files.
    """    
    def setUp(self):
        self.dataset = GoesDataSet()
        self.dataset.compile(TEST_ROOT, FILENAMES)
        self.start   = "2013-02-27 23:50"
        self.end     = "2013-02-28 00:10"
        self.records = 5
    
    def test_returns_a_table(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertIsInstance(actual, Table)

    def test_correct_number_of_records(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(len(actual), self.records)
    
    def test_files_in_date_order(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)

    def test_files_not_in_date_order(self):
        reversed_dataset = GoesDataSet()
        reversed_dataset.compile(TEST_ROOT, reversed(FILENAMES))
        actual = reversed_dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)


class TestGoesFile(unittest.TestCase):
    """ 
    Test the GoesFile class instantiates and handles errors
    """
    def test_requires_path(self):
        with self.assertRaises(TypeError):
            GoesFile()

    def test_incorrect_path_filename(self):
        with self.assertRaises(IOError):
            GoesFile(os.path.join(TEST_ROOT, 'wrong_filename.txt'))

    def test_blank_path_filename(self):
        with self.assertRaises(IOError):
            GoesFile(os.path.join(TEST_ROOT, ''))

    def test_invalid_path_type(self):
        with self.assertRaises(IOError):
            GoesFile('/invalid')

    def test_incomplete_path(self):
        with self.assertRaises(IOError):
            GoesFile(TEST_ROOT)

    def test_exists(self):
        test_file = os.path.join(TEST_ROOT, '20130227_Gp_xr_5m.txt')
        self.assert_(GoesFile(test_file))


class TestGoesFileFormatting(unittest.TestCase):
    """ 
    Test the data the GoesFile class imports, how it 
    formats it, and accesses the results.
    """
    def setUp(self):
        self.goes = GoesFile(os.path.join(TEST_ROOT, FILENAMES[0]))
        self.glength = 288

    def test_length(self):
        self.assertEqual(self.glength, len(self.goes.table))

    def test_original_columns(self):
        expected = ['col1', 'col2', 'col3', 'col4', 
                    'col5', 'col6', 'col7', 'col8']
        actual = sorted(self.goes.columns.keys())
        self.assertEqual(expected, actual)
        
    def test_new_columns(self):
        expected = ('year', 'month', 'day', 'time',
                    'JD days', 'JD secs',
                    '0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)',
                    'datetime', 'Modified JD')
        actual = self.goes.table.names
        self.assertEqual(expected, actual)

    def test_first_datetime(self):
        actual = self.goes.table.datetime[0]
        self.assertEqual("2013-02-27 00:00", actual)
        
    def test_last_datetime(self):
        actual = self.goes.table.datetime[self.glength - 1]
        self.assertEqual("2013-02-27 23:55", actual)
        
    def test_get_date_range(self):
        start   = "2013-02-27 00:30"
        end     = "2013-02-27 01:00"
        actual = self.goes.get_date_range(start, end)
        self.assertIsInstance(actual, Table)
        self.assertEqual(actual.datetime[0], start)
        self.assertEqual(len(actual), 7)
        self.assertEqual(actual.datetime[6], end)

    def test_first_modified_jd(self):
        actual = self.goes.table['Modified JD'][0]
        self.assertEqual(56350.00000, actual)
        
    def test_last_modified_jd(self):
        actual = self.goes.table['Modified JD'][287]
        self.assertEqual(56350.99653, actual)
        