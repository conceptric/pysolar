import os

from pygoes.files.configuration import Configuration

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
REMOTE = "http://www.swpc.noaa.gov/ftpdir/lists/xray/"
TEST_CONFIG = { 'source'       : REMOTE,
                'cache'        : FIXTURES,
                'file_template': "Gp_xr_%sm.txt" }

def get_mock_config():
    return Configuration(TEST_CONFIG)
    
def get_cached_path(filename):
    return os.path.join(FIXTURES, filename)
    
def cached_file_exists(filename):
    return os.path.exists(get_cached_path(filename))

def get_cached_mtime(filename):
    return os.path.getmtime(get_cached_path(filename))
