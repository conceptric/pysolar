import urllib2
from repository import RemoteManager
from cache import CacheManager

class Downloader:
    """
    Downloads named files from a specified remote location.
    config: An instance of the Configuration class.
    """
    def __init__(self, remote, cache):
        self.remote = remote
        self.cache = cache

    def download(self, filename):
        ''' 
        Downloads a single named file from a remote location. 
        Takes a string for the filename.
        '''
        if not self.cache.file_exists(filename):
            content = self.remote.read(filename)
            self.cache.write_file(filename, content)


class FileManager:
    """ 
    Builds more complex file download behaviours.
    config: An instance of the Configuration class.
    """
    def __init__(self, config):
        self.downloader = Downloader(remote=RemoteManager(config),
                                     cache=CacheManager(config))
        self.template = config.file_template

    def download(self, filename):
        ''' 
        Delegates this method to be Downloader class. Takes 
        a filename string.
        '''
        self.downloader.download(filename)
        
    def download_by_name(self, filenames):
        '''
        Takes a list of file name strings and iterates 
        through the download method.
        '''
        for file in filenames:
            self.download(file)

    def download_by_template(self, strings):
        '''
        Takes a list of strings, generates a list of file 
        names with the configuration template and passes it 
        to the file_by_name methods for download.
        '''
        filenames = self.filenames_from_template(strings)
        self.download_by_name(filenames)        
        
    def filenames_from_template(self, strings):
        '''
        Takes a list of strings and maps the configuration 
        template onto them to generate a list of file names.
        '''
        return map(lambda f: self.template % (f), strings)
