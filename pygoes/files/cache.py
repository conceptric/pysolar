import os

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
            cache = open(os.path.join(self.path, filename), 'w')
            cache.write(data)
            cache.close()
        