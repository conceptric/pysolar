import os

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
REMOTE = "http://www.swpc.noaa.gov/ftpdir/lists/xray/"

class MockRemoteConfig:
    def __init__(self):
        self.source = REMOTE
        self.cache = FIXTURES
        self.file_template = "Gp_xr_%sm.txt"

