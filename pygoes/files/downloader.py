import urllib2
from pygoes.utils.errors import MissingFileError
from repository import RemoteManager
from cache import CacheManager

class DownloadManager:
    """ 
    Coordinator class for the files package downloads
    """
    def __init__(self, config):
        self.remote = RemoteManager(config)
        self.cache = CacheManager(config)

    def download(self, filename):
        if not self.cache.file_exists(filename):
            remote = self.remote.read(filename)
            self.cache.write_file(filename, remote)

    def files_by_name(self, filenames):
        for file in filenames:
            self.download(file)