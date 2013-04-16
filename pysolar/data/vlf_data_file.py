import atpy

class VlfDataFile(object):
    """
    Class to represent a VLF comma-delimited data file using 
    ATPy tables.
    
    On creation it reads the file data from the path including the headers.
    
    path    : path to the data file.

    The table attribute contains the ATPy table instance.
    """
    def __init__(self, path):
        self.table = atpy.Table(path, type="ascii", delimiter=",")
        
        
