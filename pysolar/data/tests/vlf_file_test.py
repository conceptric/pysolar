import unittest
from numpy import datetime64

from data_test_config import *
from pysolar.data import VlfFile


class TestDateTimeMethods(unittest.TestCase):
    " Test methods for manipulating date time data. "
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.vlf = VlfFile(test_file)

    def test_all_dates_are_numpy_format(self):
        dates = self.vlf.all_dates()
        for d in dates:
            self.assertIsInstance(d, datetime64)

    def test_begins(self):
        expected = datetime64('2013-03-23 19:12:43')
        self.assertEqual(expected, self.vlf.begins())

    def test_finishes(self):
        expected = datetime64('2013-03-23 19:13:28')
        self.assertEqual(expected, self.vlf.finishes())


class TestRecordSelectionMethods(unittest.TestCase):
    """ Test methods for selecting data records """
    def setUp(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.vlf = VlfFile(test_file)
    
    def test_select_a_single_record_by_datetime(self):
        expected = '2013-03-23 19:12:43'
        selection = self.vlf.select_between_dates(start=expected)
        self.assertEqual(1, len(selection))
        self.assertEqual(expected, selection['Date_Time'])

    def test_select_records_from_middle_of_the_file_by_datetime(self):
        expected_start = '2013-03-23 19:12:58'
        expected_end = '2013-03-23 19:13:13'
        selection = self.vlf.select_between_dates(start=expected_start, 
        end=expected_end)
        self.assertEqual(2, len(selection))
        self.assertEqual(expected_start, selection['Date_Time'][0])
        self.assertEqual(expected_end, selection['Date_Time'][1])
        

if __name__ == '__main__':
    unittest.main()        