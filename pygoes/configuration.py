
class FileDownloadSettings:
    """ 
    Class that contains the details of a file 
    to be downloaded 
    """
    def __init__(self, url, cache_path):
        self.source = url
        self.cache = cache_path
