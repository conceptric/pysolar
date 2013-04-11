import os
import urllib2
from contextlib import closing

from pysolar.files.utils import MissingFileError

class FileManager:
    """ 
    Builds more complex file download behaviours.
    config: An instance of the Configuration class.
    """
    def __init__(self, config):
        self.remote = RemoteManager(config)
        self.cache = CacheManager(config)
        self.template = config.file_template

    def download(self, filenames):
        ''' 
        Takes a list of file name strings and iterates 
        through the cache download method.
        '''
        for filename in filenames:
            self.cache.download(filename, self.remote)
        
    def download_by_template(self, strings):
        '''
        Takes a list of strings, generates a list of file 
        names with the configuration template and passes it 
        to the file_by_name methods for download.
        '''
        filenames = self.filenames_from_template(strings)
        self.download(filenames)        
        
    def filenames_from_template(self, strings):
        '''
        Takes a list of strings and maps the configuration 
        template onto them to generate a list of file names.
        '''
        return map(lambda f: self.template % (f), strings)


class CacheManager:
    """
    Class to manage the local data file cache.
    """
    def __init__(self, config):
        '''
        Checks if the cache path provided in the configuration 
        exists. Raises a ValueError if not.
        '''
        if os.path.exists(config.cache):
            self.path = config.cache
        else:
            raise ValueError("Cache directory does not exist.")

    def file_exists(self, filename):
        ''' 
        Checks whether a file named with the string filename 
        exists in the local cache. 
        Returns True if it exists or False if not.
        '''
        return os.path.exists(os.path.join(self.path, filename))
        
    def write_file(self, filename, data):
        '''
        Write a file to the local cache only if it does not 
        already exists.
        filename: string defining the name of the file.
        data    : string for the contents of the new file.
        '''
        if not self.file_exists(filename):
            with closing(self.__open(filename, 'w')) as cached:
                cached.write(data)
    
    def read(self, filename):
        '''
        Read the contents of a named file from the local cache.
        filename: string defining the name of the file.        
        '''
        with closing(self.__open(filename)) as cached:
            return cached.read()        

    def download(self, filename, remote):
        ''' 
        Downloads a single named file from a remote location. 
        filename: a string for the filename.
        remote  : a remote repository object.
        '''
        if not self.file_exists(filename):
            content = remote.read(filename)
            self.write_file(filename, content)
        
    def __open(self, filename, op='r'):
        return open(os.path.join(self.path, filename), op)


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

