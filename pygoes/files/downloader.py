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
        self.template = config.file_template

    def download(self, filename):
        if not self.cache.file_exists(filename):
            remote = self.remote.read(filename)
            self.cache.write_file(filename, remote)

    def files_by_name(self, filenames):
        for file in filenames:
            self.download(file)

    def files_by_template(self, strings):
        filenames = self.filenames_from_template(strings)
        self.files_by_name(filenames)        
        
    def filenames_from_template(self, strings):
        return map(lambda f: self.template % (f), strings)
