import urllib2
from repository import *

class FileManager:
    """ 
    Builds more complex file download behaviours.
    config: An instance of the Configuration class.
    """
    def __init__(self, config):
        self.remote = RemoteManager(config)
        self.cache = CacheManager(config)
        self.template = config.file_template

    def download(self, filename):
        ''' 
        Delegates this method to be Downloader class. Takes 
        a filename string.
        '''
        self.cache.download(filename, self.remote)
        
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
