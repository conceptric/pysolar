import urllib2

class RemoteManager:
    """
    Class that represents a remote repository of data files.
    """
    def __init__(self, settings):
        self.url = settings.source

    def open(self, filename):
        return urllib2.urlopen(self.url + '/' + filename)
    
    def read(self, filename):
        remote = self.open(filename)
        content = remote.read()        
        remote.close()        
        return content

