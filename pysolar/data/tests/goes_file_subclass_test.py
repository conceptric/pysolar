import unittest

from data_test_config import *
from pysolar.data import *


class TestAnXrayGoesFile(unittest.TestCase):
    """ 
    Test that the GoesFile imports the XRay data properly.
    """
    def setUp(self):
        self.goes = XrayGoesFile(os.path.join(FIXTURES, '20130227_Gp_xr_5m.txt'))
        self.glength = 288

    def test_file_length(self):
        self.assertEqual(self.glength, self.goes.size())
        
    def test_xray_data_column_names_exist(self):
        expected = ('0.05-0.4 nanometer (W/m2)',
                    '0.1-0.8 nanometer (W/m2)')
        actual = self.goes.names
        for item in expected:
            self.assertTrue(item in actual, "'%s' is missing" % (item))


class TestAMagneticGoesFile(unittest.TestCase):
    """ 
    Test that the GoesFile imports the Magnetometry data properly.
    """
    def setUp(self):
        self.goes = MagneticGoesFile(os.path.join(FIXTURES, '20130322_Gp_mag_1m.txt'))
        self.glength = 1440

    def test_file_length(self):
        self.assertEqual(self.glength, self.goes.size())
        
    def test_magnetic_data_column_names_exist(self):
        expected = ('Hp (nT)', 'He (nT)', 'Hn (nT)',
                    'Total Field (nT)')
        actual = self.goes.names
        for item in expected:
            self.assertTrue(item in actual, "'%s' is missing" % (item))


if __name__ == '__main__':
    unittest.main()