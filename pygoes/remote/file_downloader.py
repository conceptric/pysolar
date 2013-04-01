import os
import urllib2
from pygoes.utils.errors import MissingFileError

class FileDownloadSettings:
    """ 
    Class that contains the details of a file 
    to be downloaded 
    """
    def __init__(self, url, cache_path):
        self.source = url
        self.cache = cache_path


class NamedFileDownloader:
    """ 
    Class that downloads the requested file 
    """
    def __init__(self, settings):
        self.settings = settings

    def __open_remote(self, filename):
        return urllib2.urlopen(self.settings.source + '/' + filename)

    def __path_to_cached_file(self, filename):
        return os.path.join(self.settings.cache, filename)

    def already_cached(self, filename):
        return os.path.exists(self.__path_to_cached_file(filename))
    
    def read_remote(self, filename):
        remote = self.__open_remote(filename)
        content = remote.read()        
        remote.close()        
        return content

    def write_cached(self, filename, content):
        cache = open(self.__path_to_cached_file(filename), 'w')
        cache.write(content)
        cache.close()

    def __handle_http_error(self, http_error, filename):
        if http_error.code == 404:
            raise MissingFileError("%s is missing in the remote location." % filename)
        else:
            raise        
            
    def download(self, filename):
        try:
            remote = self.read_remote(filename)
            self.write_cached(filename, remote)
        except urllib2.HTTPError as ex:
            self.__handle_http_error(ex, filename)