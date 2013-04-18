import unittest
from numpy import datetime64

from data_test_config import *
from pysolar.data import VlfFile


class TestModifiedJulianDate(unittest.TestCase):
    " Test that a modified JD field is added to the table "        
    def setUp(self):
        path = os.path.join(FIXTURES, 'example_vlf_data.txt')
        self.vlf = VlfFile(path)
        
    def test_simple_modified_julian_date(self):
        datetime = datetime64('2013-03-22 00:00')
        expected = 56373.0
        actual = self.vlf.modified_julian_day(datetime)
        self.assertEqual(expected, actual, 'The Julian Date is wrong')

    def test_tricky_modified_julian_date(self):
        datetime = datetime64('2013-02-28 00:45')
        expected = 56351.03125
        actual = self.vlf.modified_julian_day(datetime)
        self.assertEqual(expected, actual)

    def test_modified_column_names(self):
        expected = 'ModifiedJD'
        actual = self.vlf.names()
        self.assertTrue(expected in actual, "'%s' is missing" % (expected))

    def test_modifiedjd_column_has_proper_days(self):
        datetime = datetime64('2013-03-23 19:12:43')
        expected = self.vlf.modified_julian_day(datetime)
        actual = self.vlf.table.ModifiedJD[0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()        