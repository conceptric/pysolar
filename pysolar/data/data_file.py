import atpy
from numpy import datetime64

class DataFile(object):
    """
    Class to represent the contents of a data file and 
    provide basic methods to query and manipulate these 
    data using ATPy tables.
    
    path        : path to the data file.
    delimiter   : optional data delimiter, defaults to ",".
    header_start: optional position of header row, defaults to 0.
    data_start  : optional position of first data row, defaults to 1.
     
    The table attribute contains the ATPy table instance.           
    """
    def __init__(self, path, delimiter=',', header_start=0, data_start=1):
        self.datetime_label = 'Date_Time'   
        self.table = self.__read(path, delimiter, header_start, data_start)
    
    def __read(self, path, delimiter, header_start, data_start):
        data = atpy.Table(path, type="ascii", delimiter=delimiter, 
        header_start=header_start, data_start=data_start)
        return data
        
    def size(self):
        ' Returns an integer for the number of records '
        return len(self.table)

    def names(self):
        ' Returns the names of the fields in the table attribute '
        return self.table.names
        
    def all_dates(self):
        ' Returns a numpy array containing all the datetimes '
        return self.table[self.datetime_label].astype(datetime64)

    def begins(self):
        ' Returns the earliest datetime in the file '
        return self.all_dates().min()

    def finishes(self):
        ' Returns the latest datetime in the file '
        return self.all_dates().max()

        
