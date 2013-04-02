import urllib2
from contextlib import closing

from pygoes.utils.errors import MissingFileError

class RemoteManager:
    """
    Class that represents a remote repository of data files.
    """
    def __init__(self, settings):
        urllib2.urlopen(urllib2.Request(settings.source))
        self.url = settings.source

    def read(self, filename):
        with closing(self.__open(filename)) as remote:
            content = remote.read()        
            return content

    def __open(self, filename):
        try:
            return urllib2.urlopen(self.url + '/' + filename)
        except urllib2.HTTPError as ex:
            self.__handle_http_error(ex, filename)

    def __handle_http_error(self, http_error, filename):
        if http_error.code == 404:
            raise MissingFileError("%s is missing in the remote location." % 
                filename)
        else:
            raise        
