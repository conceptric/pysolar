import unittest
import os
from numpy import datetime64
from asciitable import InconsistentTableError

from data_test_config import *
from pysolar.utils.datetime import *
from pysolar.data import DataFile, DataTable

class TestDataFile(unittest.TestCase):
    """
    Tests the basic error handling of the DataSet class.
    """
    def test_requires_path(self):
        with self.assertRaises(TypeError):
            DataFile()

    def test_incorrect_path_filename(self):
        with self.assertRaises(IOError):
            DataFile(os.path.join(FIXTURES, 'wrong_filename.txt'))

    def test_blank_path_filename(self):
        with self.assertRaises(IOError):
            DataFile(os.path.join(FIXTURES, ''))

    def test_invalid_path_type(self):
        with self.assertRaises(IOError):
            DataFile('/invalid')

    def test_incomplete_path(self):
        with self.assertRaises(IOError):
            DataFile(FIXTURES)

    def test_empty_file(self):
        test_file = os.path.join(FIXTURES, 'empty_file.txt')
        with self.assertRaises(InconsistentTableError):
            DataFile(test_file)

class TestValidDataFile(unittest.TestCase):
    """
    Tests the basic functionality of the DataSet class.
    """
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.datafile = DataFile(test_file)
        
    def test_size(self):
        ' Test the number of records in a valid file '
        self.assertEqual(4, self.datafile.size())
    
    def test_names(self):
        ' Test that the names can be retrieved from the table '
        expected = ('Date_Time', 'Noise', 'ICV', 'ModifiedJD')
        self.assertEqual(expected, self.datafile.names)
        
    def test_has_column(self):
        self.assertTrue(self.datafile.has_column('Date_Time'))
        self.assertFalse(self.datafile.has_column('HWU'))


class TestDateTimeMethods(unittest.TestCase):
    " Test methods for manipulating date time data. "
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.datafile = DataFile(test_file)

    def test_all_dates_are_numpy_format(self):
        dates = self.datafile.all_dates()
        for d in dates:
            self.assertIsInstance(d, datetime64)

    def test_begins(self):
        expected = datetime64('2013-03-23 19:12:43')
        self.assertEqual(expected, self.datafile.begins())

    def test_finishes(self):
        expected = datetime64('2013-03-23 19:13:28')
        self.assertEqual(expected, self.datafile.finishes())
        
    def test_dates_as_mjd(self):
        expected = modified_julian_day(datetime64('2013-03-23 19:12:43'))
        dates = self.datafile.dates_as_mjd()
        self.assertEqual(expected, dates[0])
        self.assertEqual(4, len(dates))

    def test_dates_as_mjd_with_invalid_datetime_label(self):
        self.datafile.datetime_label = 'datetime'
        with self.assertRaises(IndexError):
            self.datafile.dates_as_mjd()


class TestSortingMethods(unittest.TestCase):
    " Test methods for sorting data. "
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'out_of_sequence_data.txt')
        self.datafile = DataFile(test_file)

    def test_reading_out_of_sequence_data(self):
        expected_start = np.datetime64('2013-03-23 19:12:58')
        expected_end = np.datetime64('2013-03-23 19:13:13')
        dates = self.datafile.all_dates()
        self.assertEqual(4, len(dates))
        self.assertEqual(expected_start, dates[0])
        self.assertEqual(expected_end, dates[3])

    def test_reading_out_of_sequence_data(self):
        expected_start = np.datetime64('2013-03-23 19:12:43')
        expected_end = np.datetime64('2013-03-23 19:13:28')
        self.datafile.sort_by_mjd()
        dates = self.datafile.all_dates()
        self.assertEqual(4, len(dates))
        self.assertEqual(expected_start, dates[0])
        self.assertEqual(expected_end, dates[3])
        

class TestRecordSelectionMethods(unittest.TestCase):
    """ Test methods for selecting data records """
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.datafile = DataFile(test_file)
    
    def test_select_a_single_record_by_datetime(self):
        expected = '2013-03-23 19:12:43'
        selection = self.datafile.select_between_dates(start=expected)
        self.assertEqual(1, selection.size())
        self.assertEqual(expected, selection['Date_Time'])

    def test_select_records_from_middle_of_the_file_by_datetime(self):
        expected_start = '2013-03-23 19:12:58'
        expected_end = '2013-03-23 19:13:13'
        selection = self.datafile.select_between_dates(start=expected_start, 
        end=expected_end)
        self.assertEqual(2, selection.size())
        self.assertEqual(expected_start, selection['Date_Time'][0])
        self.assertEqual(expected_end, selection['Date_Time'][1])
        
    def test_invalid_datetime_type(self):
        start   = "invalid"
        end     = "2013-03-23 19:13:13"
        with self.assertRaises(ValueError):
            self.datafile.select_between_dates(start, end)        

    def test_invalid_datetime(self):
        start       = "2013-03-23 19:13:13"
        invalid_end = "2013-02-27 24:55:59"
        with self.assertRaises(ValueError):
            self.datafile.select_between_dates(start, invalid_end)        

    def test_start_is_after_the_end_datetime(self):
        start   = "2013-03-23 19:13:13"
        end     = "2013-03-23 19:12:58"
        with self.assertRaises(ValueError):
            self.datafile.select_between_dates(start, end)        


if __name__ == '__main__':
    unittest.main()