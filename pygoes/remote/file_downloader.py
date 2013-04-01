import os
import urllib2
from pygoes.utils.errors import MissingFileError

class CacheManager:
    """
    Class to manage the local data file cache.
    """
    def __init__(self, settings):
        self.path = settings.cache

    def file_exists(self, filename):
        return os.path.exists(os.path.join(self.path, filename))
        
    def write_file(self, filename, data):
        cache = open(os.path.join(self.path, filename), 'w')
        cache.write(data)
        cache.close()
            

class NamedFileDownloader:
    """ 
    Class that downloads the requested file 
    """
    def __init__(self, settings):
        self.settings = settings
        self.cache = CacheManager(settings)

    def __open_remote(self, filename):
        return urllib2.urlopen(self.settings.source + '/' + filename)

    def already_cached(self, filename):
        return self.cache.file_exists(filename)
    
    def read_remote(self, filename):
        remote = self.__open_remote(filename)
        content = remote.read()        
        remote.close()        
        return content

    def __handle_http_error(self, http_error, filename):
        if http_error.code == 404:
            raise MissingFileError("%s is missing in the remote location." % filename)
        else:
            raise        
            
    def download(self, filename):
        if not self.cache.file_exists(filename):
            try:
                remote = self.read_remote(filename)
                self.cache.write_file(filename, remote)
            except urllib2.HTTPError as ex:
                self.__handle_http_error(ex, filename)