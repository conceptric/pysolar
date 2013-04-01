import urllib2
from pygoes.utils.errors import MissingFileError

class NamedFileDownloader:
    """ 
    Class that downloads the requested file.
    """
    def __init__(self, remote_manager, cache_manager):
        self.remote = remote_manager
        self.cache = cache_manager

    def __handle_http_error(self, http_error, filename):
        if http_error.code == 404:
            raise MissingFileError("%s is missing in the remote location." % filename)
        else:
            raise        
            
    def download(self, filename):
        if not self.cache.file_exists(filename):
            try:
                remote = self.remote.read(filename)
                self.cache.write_file(filename, remote)
            except urllib2.HTTPError as ex:
                self.__handle_http_error(ex, filename)