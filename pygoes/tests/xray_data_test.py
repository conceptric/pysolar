import unittest
import os
from atpy.basetable import Table
from asciitable import InconsistentTableError
from pygoes.xray.data import GoesFile

TEST_ROOT = os.path.dirname(__file__)
FILENAMES =  ['20130227_Gp_xr_5m.txt']

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
        test_file = os.path.join(TEST_ROOT, FILENAMES[0])
        self.assert_(GoesFile(test_file))

    def test_empty_file(self):
        test_file = os.path.join(TEST_ROOT, 'empty_file.txt')
        with self.assertRaises(InconsistentTableError):
            GoesFile(test_file)

class TestGoesFileFormatting(unittest.TestCase):
    """ 
    Test the data the GoesFile class imports, and how it 
    formats it.
    """
    def setUp(self):
        self.goes = GoesFile(os.path.join(TEST_ROOT, FILENAMES[0]))
        self.glength = 288

    def test_file_length(self):
        self.assertEqual(self.glength, len(self.goes.table))
        
    def test_original_column_names(self):
        expected = ['col1', 'col2', 'col3', 'col4', 
                    'col5', 'col6', 'col7', 'col8']
        actual = sorted(self.goes.columns.keys())
        self.assertEqual(expected, actual)
        
    def test_modified_column_names(self):
        expected = ('year', 'month', 'day', 'time',
                    'JD days', 'JD secs',
                    '0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)',
                    'datetime', 'Modified JD')
        actual = self.goes.table.names
        self.assertEqual(expected, actual)

    def test_datetime_of_the_first_record(self):
        actual = self.goes.table.datetime[0]
        self.assertEqual("2013-02-27 00:00", actual)
        
    def test_datetime_of_the_last_record(self):
        actual = self.goes.table.datetime[self.glength - 1]
        self.assertEqual("2013-02-27 23:55", actual)

class TestGoesFileReading(unittest.TestCase):
    """ 
    Test the data the GoesFile class accesses its contents.
    """        
    def setUp(self):
        self.goes = GoesFile(os.path.join(TEST_ROOT, FILENAMES[0]))

    def test_get_date_range(self):
        start   = "2013-02-27 00:30"
        end     = "2013-02-27 01:00"
        actual = self.goes.get_date_range(start, end)
        self.assertIsInstance(actual, Table)
        self.assertEqual(actual.datetime[0], start)
        self.assertEqual(len(actual), 7)
        self.assertEqual(actual.datetime[6], end)

    def test_invalid_datetime_format(self):
        start   = "invalid"
        end     = "2013-02-27 01:00"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_invalid_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 24:55"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_start_is_after_the_end_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 23:40"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_first_modified_jd(self):
        actual = self.goes.table['Modified JD'][0]
        self.assertEqual(56350.00000, actual)
        
    def test_last_modified_jd(self):
        actual = self.goes.table['Modified JD'][287]
        self.assertEqual(56350.99653, actual)
        