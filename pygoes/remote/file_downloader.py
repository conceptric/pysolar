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
            remote = self.__open_remote()
            return True
        except urllib2.HTTPError:
            return False
        finally:
            remote.close()

    def __open_remote(self):
        return urllib2.urlopen(self.source)

    def local_exists(self):
        return os.path.exists(self.destination)
        
    def download(self):
        local = open(self.destination, 'w')
        remote = self.__open_remote()
        local.write(remote.read())
        remote.close()
        local.close()
        