import unittest
from pygoes.utils.datetime import DateCompiler

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
        