import unittest
import os
from asciitable import InconsistentTableError

from data_test_config import *
from pysolar.data import DataFile

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
        expected = ('Date_Time', 'Noise', 'ICV')
        self.assertEqual(expected, self.datafile.names())
    

if __name__ == '__main__':
    unittest.main()