import unittest
import os
from pygoes.xray.data import GoesFile

class TestXrayGoesFile(unittest.TestCase):
    """ Test the class that imports GOES-15 X-Ray data files """

    def setUp(self):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, '20130227_Gp_xr_5m.txt')
        self.goesfile = GoesFile(path)

    def test_exists(self):
        self.assert_(self.goesfile)
        
    def test_length(self):
        self.assertEqual(self.goesfile.size(), 288)

    def test_original_columns(self):
        expected = ['col1', 'col2', 'col3', 'col4', 'col7', 'col8']
        actual = sorted(self.goesfile.COLUMNS.keys())
        self.assertEqual(actual, expected)
        
    def test_new_columns(self):
        expected = ('year', 
                    'month',
                    'day',
                    'time',
                    '0.05- 0.4 nanometer (W/m2)',
                    '0.1 - 0.8 nanometer (W/m2)')
        actual = self.goesfile.names()
        self.assertEqual(actual, expected)