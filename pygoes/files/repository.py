import urllib2
from contextlib import closing

from pygoes.files.errors import MissingFileError

class RemoteManager:
    """
    Class that represents a remote repository of data files.
    config: An instance of the Configuration class.
    """
    def __init__(self, config):
        self.url = config.source

    def read(self, filename):
        ''' 
        Reads an existing remote file into memory.
        Raises:
          MissingFileError if the file cannot be found.
          URLError is the url is unknown.
        '''        
        with closing(self.__open(filename)) as remote:
            content = remote.read()        
            return content

    def __open(self, filename):
        ''' Raises a URLError is the url is unknown. '''
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

