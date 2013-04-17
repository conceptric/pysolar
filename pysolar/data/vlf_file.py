import atpy
import numpy as np

from pysolar.data import DataFile

class VlfFile(DataFile):
    """
    Class to represent a VLF comma-delimited data file using 
    ATPy tables.
    
    On creation it reads the file data from the path including the headers.
    
    path    : path to the data file.

    The table attribute contains the ATPy table instance.
    """
    def __init__(self, path):
        super(VlfFile, self).__init__(path)
        
        