import unittest
from pysolar.utils.datetime import *
from numpy import datetime64


class TestModifiedJulianDay(unittest.TestCase):
    " Test that a modified Julian day function "        
    def test_simple_modified_julian_day(self):
        expected = 56373.0
        actual = modified_julian_day(datetime64('2013-03-22 00:00'))
        self.assertEqual(expected, actual, 'The Julian Date is wrong')

    def test_tricky_modified_julian_day(self):
        expected = 56351.03125
        actual = modified_julian_day(datetime64('2013-02-28 00:45'))
        self.assertEqual(expected, actual)


class TestDateCompilerDatetimes(unittest.TestCase):
    """ 
    Tests the Datetime string handling methods of 
    the DateCompiler class.
    """
    
    def test_basic_datetime(self):
        components = {'year': 2013,
                      'month': 12,
                      'day': 20,
                      'time': 1645}
        expected = "2013-12-20 16:45"
        actual = DateCompiler().build_datetime(components)
        self.assertEqual(expected, actual)
        
    def test_datetime_with_single_digits(self):
        components = {'year': 2013,
                      'month': 2,
                      'day': 2,
                      'time': 10}
        expected = "2013-02-02 00:10"
        actual = DateCompiler().build_datetime(components)
        self.assertEqual(expected, actual)

class TestDateCompilerJulianDate(unittest.TestCase):
    """ 
    Tests the Julian Date methods of the DateCompiler class.
    """

    def test_with_no_seconds(self):
        components = { 'JD days': 56351, 'JD secs': 0 }
        actual = DateCompiler().modified_julian_date(components)
        self.assertEqual(56351.00000, actual)
        
    def test_with_maximum_seconds(self):
        components = { 'JD days': 56351, 'JD secs': 86399 }
        actual = DateCompiler().modified_julian_date(components)
        self.assertEqual(56351.99999, actual)    
        