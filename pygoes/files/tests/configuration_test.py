import unittest
import os

from pygoes.files.configuration import Configuration
from remote_test_config import *

class TestConfigurationDefaults(unittest.TestCase):
    """
    Test the Files package configuration class defaults.
    """
    def setUp(self):
        self.config = Configuration()
        
    def test_it_has_a_default_source_attribute(self):
        self.assertEqual(self.config.source, '')

    def test_it_has_a_default_cache_attribute(self):
        ''' Default is the local working directory '''
        self.assertEqual(self.config.cache, os.getcwd())

    def test_it_has_a_default_file_template_attribute(self):
        ''' 
        Default should return the supplied string to 
        prevent errors
        '''
        self.assertEqual(self.config.file_template, '%s')


class TestConfigurationArguments(unittest.TestCase):
    """
    Test the Files package configuration class with attributes 
    passed in as a dictionary.
    """
    def test_it_uses_the_passed_in_source(self):
        config = Configuration({'source': REMOTE})
        self.assertEqual(config.source , REMOTE)
        
    def test_it_uses_the_passed_in_cache(self):
        config = Configuration({'cache': FIXTURES})
        self.assertEqual(config.cache , FIXTURES)
        
    def test_it_uses_the_passed_in_template(self):            
        config = Configuration({'file_template': '%s_test.txt'})
        self.assertEqual(config.file_template , '%s_test.txt')

    def test_it_uses_a_whole_set_of_passed_in_attributes(self):            
        attributes = {  'source': REMOTE, 
                        'cache': FIXTURES, 
                        'file_template': '%s.txt' }
        config = Configuration(attributes)
        self.assertEqual(config.source , REMOTE)
        self.assertEqual(config.cache , FIXTURES)
        self.assertEqual(config.file_template , '%s.txt')
