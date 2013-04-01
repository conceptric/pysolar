import os

class CacheManager:
    """
    Class to manage the local data file cache.
    """
    def __init__(self, settings):
        self.path = settings.cache

    def file_exists(self, filename):
        return os.path.exists(os.path.join(self.path, filename))
        
    def write_file(self, filename, data):
        if not self.file_exists(filename):
            cache = open(os.path.join(self.path, filename), 'w')
            cache.write(data)
            cache.close()
        