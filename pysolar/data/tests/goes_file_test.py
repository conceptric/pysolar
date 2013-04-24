import unittest

from data_test_config import *
from pysolar.data import *

XRAY =  '20130227_Gp_xr_5m.txt'

class TestGoesFile(unittest.TestCase):
    """ 
    Test the GoesFile class instance
    """
    def setUp(self):
        self.goes = GoesFile(os.path.join(FIXTURES, XRAY))
        
    def test_defaults_to_a_date_column_map(self):        
        column_map = self.goes.get_column_map()
        expected = {'col1': 'year',
                    'col2': 'month',
                    'col3': 'day', 
                    'col4': 'time',
                    'col5': 'JD days',
                    'col6': 'JD secs'}
        self.assertEquals(column_map, expected)

    def test_modified_column_names(self):
         expected = ('year', 'month', 'day', 'time',
                     'JD days', 'JD secs', 'Date_Time', 'ModifiedJD')
         actual = self.goes.names
         for item in expected:
             self.assertTrue(item in actual, "'%s' is missing" % (item))

    def test_datetime_of_the_first_record(self):
        actual = self.goes.begins()
        self.assertEqual("2013-02-27T00:00Z", actual.astype(str))

    def test_datetime_of_the_last_record(self):
        actual = self.goes.finishes()
        self.assertEqual("2013-02-27T23:55Z", actual.astype(str))


class TestGoesFileGetDateRange(unittest.TestCase):
    """ 
    Test the data the GoesFile class accesses its contents by
    date ranges.
    """        
    def setUp(self):
        self.goes = GoesFile(os.path.join(FIXTURES, XRAY))

    def test_select_between_dates(self):
        start   = "2013-02-27 00:30"
        end     = "2013-02-27 01:00"
        actual = self.goes.select_between_dates(start, end)
        self.assertEqual(actual['Date_Time'][0], start)
        self.assertEqual(len(actual), 7)
        self.assertEqual(actual.Date_Time[6], end)

    def test_invalid_datetime_format(self):
        start   = "invalid"
        end     = "2013-02-27 01:00"
        with self.assertRaises(ValueError):
            self.goes.select_between_dates(start, end)        

    def test_invalid_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 24:55"
        with self.assertRaises(ValueError):
            self.goes.select_between_dates(start, end)        

    def test_start_is_after_the_end_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 23:40"
        with self.assertRaises(ValueError):
            self.goes.select_between_dates(start, end)        

    def test_first_modified_jd(self):
        actual = self.goes.table.ModifiedJD[0]
        self.assertEqual(56350.00000, actual)
        
    def test_last_modified_jd(self):
        actual = self.goes.table.ModifiedJD[287]
        self.assertEqual(56350.99653, actual)


if __name__ == '__main__':
    unittest.main()        