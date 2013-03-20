import unittest
from pygoes.xray.datetime import DateCompiler

class TestDateCompiler(unittest.TestCase):
    ''' Tests a Class to compiler datetime strings from components '''
    
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
            