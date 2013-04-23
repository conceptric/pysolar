import unittest

from data_test_config import *
from pysolar.data import DataSet

FILENAMES = ['example_datafile_1.txt', 'example_datafile_2.txt']

class TestDataSet(unittest.TestCase):
    """ 
    Test that the DataSet class exists and has
    the correct attributes. 
    """
    def setUp(self):
        self.dataset = DataSet()
            
    def test_exists(self):
        self.assert_(self.dataset)

    def test_has_empty_datafiles_attribute(self):
        self.assertEquals(self.dataset.datafiles, [])
        

class TestCompile(unittest.TestCase):
    """ 
    Test that the DataSet class can handle compilation 
    errors and import multiple data files.
    """
    def setUp(self):
        self.dataset = DataSet()

    def test_ignores_empty_file_list(self):
        self.dataset.compile(FIXTURES, [])
        self.assertEquals(0, len(self.dataset.datafiles))

    def test_ignores_incorrect_filename_in_list(self):
        self.dataset.compile(FIXTURES, ['wrong_name.txt'])
        self.assertEquals(0, len(self.dataset.datafiles))        

    def test_add_file_to_dataset(self):
        self.dataset.compile(FIXTURES, [FILENAMES[0]])
        actual = len(self.dataset.datafiles)
        self.assertEquals(1, actual)

    def test_add_two_files_to_dataset(self):
        self.dataset.compile(FIXTURES, FILENAMES)
        actual = len(self.dataset.datafiles)
        self.assertEquals(2, actual)

class TestSelectBetweenDates(unittest.TestCase):
    """ 
    Test the methods for working with date ranges
    that spread over multiple files.
    """    
    def setUp(self):
        self.dataset = DataSet()
        self.dataset.compile(FIXTURES, FILENAMES)
        self.start   = "2013-03-28 00:04:43"
        self.end     = "2013-03-28 00:05:43"
        self.records = 5
    
    def test_correct_number_of_records(self):
        actual = self.dataset.select_between_dates(self.start, self.end)
        self.assertEqual(len(actual), self.records)
    
    def test_files_in_date_order(self):
        actual = self.dataset.select_between_dates(self.start, self.end)
        self.assertEqual(actual.Date_Time[0], self.start)
        self.assertEqual(actual.Date_Time[self.records - 1], self.end)

    def test_files_not_in_date_order(self):
        reversed_dataset = DataSet()
        reversed_dataset.compile(FIXTURES, reversed(FILENAMES))
        actual = reversed_dataset.select_between_dates(self.start, self.end)
        self.assertEqual(actual.Date_Time[0], self.start)
        self.assertEqual(actual.Date_Time[self.records - 1], self.end)


if __name__ == '__main__':
    unittest.main()