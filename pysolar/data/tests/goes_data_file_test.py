import unittest

from data_test_config import *
from pysolar.data import *

XRAY =  '20130227_Gp_xr_5m.txt'
MAG =   '20130322_Gp_mag_1m.txt'

class TestGoesFile(unittest.TestCase):
    """ 
    Test the GoesFile class instance
    """
    def test_defaults_to_a_date_column_map(self):
        goes_file = GoesFile(os.path.join(FIXTURES, XRAY))
        column_map = goes_file.get_column_map()
        expected = {'col1': 'year',
                    'col2': 'month',
                    'col3': 'day', 
                    'col4': 'time',
                    'col5': 'JD days',
                    'col6': 'JD secs'}
        self.assertEquals(column_map, expected)


class TestGoesFileGetDateRange(unittest.TestCase):
    """ 
    Test the data the GoesFile class accesses its contents by
    date ranges.
    """        
    def setUp(self):
        self.goes = GoesFile(os.path.join(FIXTURES, XRAY))

    def test_get_date_range(self):
        start   = "2013-02-27 00:30"
        end     = "2013-02-27 01:00"
        actual = self.goes.get_date_range(start, end)
        self.assertEqual(actual.datetime[0], start)
        self.assertEqual(len(actual), 7)
        self.assertEqual(actual.datetime[6], end)

    def test_invalid_datetime_format(self):
        start   = "invalid"
        end     = "2013-02-27 01:00"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_invalid_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 24:55"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_start_is_after_the_end_datetime(self):
        start   = "2013-02-27 23:50"
        end     = "2013-02-27 23:40"
        with self.assertRaises(ValueError):
            self.goes.get_date_range(start, end)        

    def test_first_modified_jd(self):
        actual = self.goes.table['Modified JD'][0]
        self.assertEqual(56350.00000, actual)
        
    def test_last_modified_jd(self):
        actual = self.goes.table['Modified JD'][287]
        self.assertEqual(56350.99653, actual)


class TestAnXrayGoesFile(unittest.TestCase):
    """ 
    Test that the GoesFile imports the XRay data properly.
    """
    def setUp(self):
        self.goes = XrayGoesFile(os.path.join(FIXTURES, XRAY))
        self.glength = 288

    def test_file_length(self):
        self.assertEqual(self.glength, self.goes.size())
        
    def test_original_column_names(self):
        expected = ['col1', 'col2', 'col3', 'col4', 
                    'col5', 'col6', 'col7', 'col8']
        actual = sorted(self.goes.get_column_map().keys())
        self.assertEqual(expected, actual)
        
    def test_modified_column_names(self):
        expected = ('year', 'month', 'day', 'time',
                    'JD days', 'JD secs',
                    '0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)',
                    'datetime', 'Modified JD')
        actual = self.goes.table.names
        self.assertEqual(expected, actual)

    def test_datetime_of_the_first_record(self):
        actual = self.goes.table.datetime[0]
        self.assertEqual("2013-02-27 00:00", actual)
        
    def test_datetime_of_the_last_record(self):
        actual = self.goes.table.datetime[self.glength - 1]
        self.assertEqual("2013-02-27 23:55", actual)

class TestAMagneticGoesFile(unittest.TestCase):
    """ 
    Test that the GoesFile imports the Magnetometry data properly.
    """
    def setUp(self):
        self.goes = MagneticGoesFile(os.path.join(FIXTURES, MAG))
        self.glength = 1440

    def test_file_length(self):
        self.assertEqual(self.glength, self.goes.size())
        
    def test_original_column_names(self):
        expected = ['col1', 'col10', 'col2', 'col3', 'col4', 
                    'col5', 'col6', 'col7', 'col8',
                    'col9']
        actual = sorted(self.goes.get_column_map().keys())
        self.assertEqual(expected, actual)
        
    def test_modified_column_names(self):
        expected = ('year', 'month', 'day', 'time',
                    'JD days', 'JD secs',
                    'Hp (nT)', 'He (nT)', 'Hn (nT)',
                    'Total Field (nT)',
                    'datetime', 'Modified JD')
        actual = self.goes.table.names
        self.assertEqual(expected, actual)

    def test_datetime_of_the_first_record(self):
        actual = self.goes.table.datetime[0]
        self.assertEqual("2013-03-22 00:00", actual)
        
    def test_datetime_of_the_last_record(self):
        actual = self.goes.table.datetime[self.glength - 1]
        self.assertEqual("2013-03-22 23:59", actual)


if __name__ == '__main__':
    unittest.main()        