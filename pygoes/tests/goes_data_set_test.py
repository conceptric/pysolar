import unittest
import os
from atpy.basetable import Table
from pygoes.xray.data import GoesDataSet

TEST_ROOT = os.path.dirname(__file__)
FILENAMES =  ['20130227_Gp_xr_5m.txt', '20130228_Gp_xr_5m.txt']

class TestDataSet(unittest.TestCase):
    """ 
    Test that the DataSet class exists and has
    the correct attributes. 
    """
    def setUp(self):
        self.dataset = GoesDataSet()
            
    def test_exists(self):
        self.assert_(self.dataset)

    def test_has_empty_datafiles_attribute(self):
        self.assertEquals(self.dataset.datafiles, [])

    def test_filetype_attribute_defaults_to_xray(self):
        self.assertEquals(self.dataset.filetype, 'xray')

    def test_filetype_attribute_is_magnetic(self):
        dataset = GoesDataSet('magnetic')
        self.assertEquals(dataset.filetype, 'magnetic')


class TestDataSetCompile(unittest.TestCase):
    """ 
    Test that the DataSet class can import multiple 
    GOES-15 X-Ray data files.
    """
    def setUp(self):
        self.dataset = GoesDataSet()

    def test_ignores_empty_file_list(self):
        self.dataset.compile(TEST_ROOT, [])
        self.assertEquals(0, len(self.dataset.datafiles))

    def test_ignores_incorrect_filename_in_list(self):
        self.dataset.compile(TEST_ROOT, ['wrong_name.txt'])
        self.assertEquals(0, len(self.dataset.datafiles))        

    def test_add_file_to_dataset(self):
        self.dataset.compile(TEST_ROOT, [FILENAMES[0]])
        actual = len(self.dataset.datafiles)
        self.assertEquals(1, actual)

    def test_add_two_files_to_dataset(self):
        self.dataset.compile(TEST_ROOT, FILENAMES)
        actual = len(self.dataset.datafiles)
        self.assertEquals(2, actual)


class TestDataSetCompileTypes(unittest.TestCase):
    '''
    Test that the correct types of file are compiled.
    '''        
    def test_files_contain_xray_data(self):
        dataset = GoesDataSet()
        dataset.compile(TEST_ROOT, [FILENAMES[0]])
        xray = dataset.datafiles[0].table
        self.assertIsNotNone(xray['0.1-0.8 nanometer (W/m2)'])
        
    def test_files_contain_magnetic_data(self):
        dataset = GoesDataSet('magnetic')
        dataset.compile(TEST_ROOT, ['20130322_Gp_mag_1m.txt'])
        magnetic = dataset.datafiles[0].table
        self.assertIsNotNone(magnetic['Total Field (nT)'])


class TestDataSetGetDateRanges(unittest.TestCase):
    """ 
    Test the methods for working with date ranges
    that spread over multiple files.
    """    
    def setUp(self):
        self.dataset = GoesDataSet()
        self.dataset.compile(TEST_ROOT, FILENAMES)
        self.start   = "2013-02-27 23:50"
        self.end     = "2013-02-28 00:10"
        self.records = 5
    
    def test_returns_a_table(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertIsInstance(actual, Table)

    def test_correct_number_of_records(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(len(actual), self.records)
    
    def test_files_in_date_order(self):
        actual = self.dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)

    def test_files_not_in_date_order(self):
        reversed_dataset = GoesDataSet()
        reversed_dataset.compile(TEST_ROOT, reversed(FILENAMES))
        actual = reversed_dataset.get_date_range(self.start, self.end)
        self.assertEqual(actual.datetime[0], self.start)
        self.assertEqual(actual.datetime[self.records - 1], self.end)



