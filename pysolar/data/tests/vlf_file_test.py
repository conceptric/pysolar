import unittest
from numpy import datetime64

from data_test_config import *
from pysolar.data import VlfFile
from pysolar.utils.datetime import *


class TestModifiedJulianDate(unittest.TestCase):
    " Test that a modified JD field is added to the table "        
    def setUp(self):
        path = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.vlf = VlfFile(path)
        
    def test_modified_column_names(self):
        expected = 'ModifiedJD'
        actual = self.vlf.names()
        self.assertTrue(expected in actual, "'%s' is missing" % (expected))

    def test_modifiedjd_column_has_proper_days(self):
        datetime = datetime64('2013-03-23 19:12:43')
        expected = modified_julian_day(datetime)
        actual = self.vlf.table.ModifiedJD[0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()        