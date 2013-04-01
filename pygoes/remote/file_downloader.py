import os
import urllib2

class FileDownloadSettings:
    """ 
    Class that contains the details of a file 
    to be downloaded 
    """
    def __init__(self, url, cache_path):
        self.source = url
        self.cache = cache_path


class MissingFileError(Exception):
    """ An error for when a file could not be found. """
    pass

class FileDownloader:
    """ 
    Class that downloads the requested file 
    """
    def __init__(self, settings):
        self.settings = settings

    def remote_exists(self):
        try:
            remote = self.__open_remote()
            return True
        except urllib2.HTTPError:
            return False
        finally:
            remote.close()

    def __open_remote(self, filename):
        return urllib2.urlopen(self.settings.source + '/' + filename)

    def __path_to_cached_file(self, filename):
        return os.path.join(self.settings.cache, filename)

    def local_exists(self, filename):
        return os.path.exists(self.__path_to_cached_file(filename))
        
    def download(self, filename):
        try:
            remote = self.__open_remote(filename)
            cache = open(self.__path_to_cached_file(filename), 'w')
            cache.write(remote.read())
            remote.close()
            cache.close()
        except urllib2.HTTPError as ex:
            if ex.code == 404:
                raise MissingFileError("%s is missing in the remote location." % filename)
            else:
                raise
        