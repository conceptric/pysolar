import os
import urllib2

class FileDownloader:
    """ 
    Class that downloads the requested file 
    """
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def remote_exists(self):
        try:
            urllib2.urlopen(self.source)
            return True
        except urllib2.HTTPError:
            return False

