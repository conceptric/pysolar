import urllib2
from pygoes.utils.errors import MissingFileError

class NamedFileDownloader:
    """ 
    Class that downloads the requested file.
    """
    def __init__(self, remote_manager, cache_manager):
        self.remote = remote_manager
        self.cache = cache_manager

    def download(self, filename):
        if not self.cache.file_exists(filename):
            remote = self.remote.read(filename)
            self.cache.write_file(filename, remote)
