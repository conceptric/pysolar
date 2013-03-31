import os
import urllib2

class FileDownloadSettings:
    """ 
    Class that contains the details of a file 
    to be downloaded 
    """
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


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

    def __open_remote(self):
        return urllib2.urlopen(self.settings.source)

    def local_exists(self):
        return os.path.exists(self.settings.destination)
        
    def download(self):
        local = open(self.settings.destination, 'w')
        remote = self.__open_remote()
        local.write(remote.read())
        remote.close()
        local.close()
        