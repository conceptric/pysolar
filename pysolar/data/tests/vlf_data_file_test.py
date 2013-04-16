import unittest
import os

from data_test_config import *
from pysolar.data import VlfDataFile


class TestVlfDataFile(unittest.TestCase):
    """
    Test a representation of a typical VLF comma delimited 
    data file.
    """
    def test_requires_path(self):
        with self.assertRaises(TypeError):
            VlfDataFile()

    def test_incorrect_path_filename(self):
        with self.assertRaises(IOError):
            VlfDataFile(os.path.join(FIXTURES, 'wrong_filename.txt'))

    def test_blank_path_filename(self):
        with self.assertRaises(IOError):
            VlfDataFile(os.path.join(FIXTURES, ''))

    def test_invalid_path_type(self):
        with self.assertRaises(IOError):
            VlfDataFile('/invalid')

    def test_incomplete_path(self):
        with self.assertRaises(IOError):
            VlfDataFile(FIXTURES)

    def test_with_a_valid_file_path(self):
        test_file = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.assert_(VlfDataFile(test_file))
        self.assertEqual(4, len(VlfDataFile(test_file).table))

    def test_empty_vlf_file(self):
        test_file = os.path.join(FIXTURES, 'empty_vlf_file.txt')
        self.assertEqual(0, len(VlfDataFile(test_file).table))


if __name__ == '__main__':
    unittest.main()        