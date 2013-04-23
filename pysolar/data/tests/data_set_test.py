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


if __name__ == '__main__':
    unittest.main()