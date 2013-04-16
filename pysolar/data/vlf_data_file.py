import atpy
import numpy as np

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
        
    def size(self):
        ' Returns an integer for the number of records '
        return len(self.table)

    def all_dates(self):
        ' Returns a numpy array containing all the datetimes '
        return self.table['Date_Time'].astype(np.datetime64)

    def begins(self):
        ' Returns the earliest datetime in the file '
        return self.all_dates().min()
        
    def finishes(self):
        ' Returns the latest datetime in the file '
        return self.all_dates().max()
        
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
        
        