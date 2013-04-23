import unittest
from atpy.basetable import Table

from data_test_config import *
from pysolar.data import GoesDataSet

FILENAMES =  ['20130227_Gp_xr_5m.txt', '20130228_Gp_xr_5m.txt']

class TestGoesDataSetType(unittest.TestCase):
    """ 
    Test that the GoesDataSet can instantiate with the 
    correct type. 
    """
    def setUp(self):
        self.dataset = GoesDataSet()
            
    def test_filetype_attribute_defaults_to_xray(self):
        self.assertEquals(self.dataset.filetype, 'xray')

    def test_filetype_attribute_is_magnetic(self):
        dataset = GoesDataSet('magnetic')
        self.assertEquals(dataset.filetype, 'magnetic')


class TestDataSetCompileTypes(unittest.TestCase):
    '''
    Test that the correct types of file are compiled.
    '''        
    def test_files_contain_xray_data(self):
        dataset = GoesDataSet()
        dataset.compile(FIXTURES, [FILENAMES[0]])
        xray = dataset.datafiles[0].table
        self.assertIsNotNone(xray['0.1-0.8 nanometer (W/m2)'])
        
    def test_files_contain_magnetic_data(self):
        dataset = GoesDataSet('magnetic')
        dataset.compile(FIXTURES, ['20130322_Gp_mag_1m.txt'])
        magnetic = dataset.datafiles[0].table
        self.assertIsNotNone(magnetic['Total Field (nT)'])


if __name__ == '__main__':
    unittest.main()