import urllib2
from repository import RemoteManager
from cache import CacheManager

class Downloader:
    """
    Downloads named files from a specified remote location.
    config: An instance of the Configuration class.
    """
    def __init__(self, config):
        self.remote = RemoteManager(config)
        self.cache = CacheManager(config)

    def download(self, filename):
        ''' 
        Downloads a single named file from a remote location. 
        Takes a string for the filename.
        '''
        if not self.cache.file_exists(filename):
            remote = self.remote.read(filename)
            self.cache.write_file(filename, remote)

class DownloadManager:
    """ 
    Builds more complex file download behaviours.
    downloader: An instance of the Downloader class.
    config: An instance of the Configuration class.
    """
    def __init__(self, downloader, config):
        self.downloader = downloader
        self.template = config.file_template

    def download(self, filename):
        ''' 
        Delegates this method to be Downloader class. Takes 
        a filename string.
        '''
        self.downloader.download(filename)
        
    def files_by_name(self, filenames):
        for file in filenames:
            self.download(file)

    def files_by_template(self, strings):
        filenames = self.filenames_from_template(strings)
        self.files_by_name(filenames)        
        
    def filenames_from_template(self, strings):
        return map(lambda f: self.template % (f), strings)
