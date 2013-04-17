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
        
    def select_between_dates(self, start, end=''):
        '''
        Returns the records from the start to the 
        end datetimes inclusively.
        start   : start datetime string.
        end     : optional datetime string, defaults to start.
        '''
        dates = self.all_dates()
        if end == '': end = start
        start = np.datetime64(start)
        end = np.datetime64(end)
        return self.table.where((dates >= start) & (dates <= end))
        
        