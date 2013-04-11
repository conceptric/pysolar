import unittest

from pysolar.files.utils import *

class TestGetDateRange(unittest.TestCase):
    """
    Tests a utilities module method to generate dates 
    for each day between two specified dates
    """
    def setUp(self):
        self.start = date(2013, 01, 01)
        
    def test_returns_empty_collection(self):
        ''' If start or finish are not defined '''
        self.assertEquals(get_range_of_dates(), [])
        
    def test_returns_one_date(self):
        ''' If the start and end date are the same '''
        finish = self.start
        expected = [self.start]
        dates = get_range_of_dates(self.start, finish)
        self.assertEquals(dates, expected)

    def test_returns_several_dates(self):
        ''' Collection includes the start and finish dates '''
        number_of_days = 5
        finish = self.start + timedelta(days=number_of_days)
        dates = get_range_of_dates(self.start, finish)
        self.assertEquals(len(dates), number_of_days + 1)
        self.assertEquals(dates[0], self.start)
        self.assertEquals(dates[number_of_days], finish)
        

class TestGetDateRangeStrings(unittest.TestCase):
    """
    Tests a Module method to turn a collection of dates 
    into formatted strings.
    """
    def setUp(self):
        self.start = date(2013, 01, 01)
        
    def test_returns_a_default_string(self):
        finish = self.start
        expected = ['20130101']
        strings = get_date_range_strings(self.start, finish)
        self.assertEquals(strings, expected)

    def test_returns_a_custom_format_string(self):
        ''' Custom format is optional '''
        finish = self.start
        expected = ['0113']
        strings = get_date_range_strings(self.start, finish, '%m%y')
        self.assertEquals(strings, expected)

    def test_returns_two_default_strings(self):
        finish = self.start + timedelta(days=1)
        expected = ['20130101', '20130102']
        strings = get_date_range_strings(self.start, finish)
        self.assertEquals(strings, expected)
