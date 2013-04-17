import atpy

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