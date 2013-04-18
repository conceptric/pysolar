import atpy
import numpy as np

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
        return self.table[self.datetime_label].astype(np.datetime64)

    def begins(self):
        ' Returns the earliest datetime in the file '
        return self.all_dates().min()

    def finishes(self):
        ' Returns the latest datetime in the file '
        return self.all_dates().max()

    def select_between_dates(self, start, end=''):
        ''' 
        Returns a table containing records from the start to the 
        end datetimes inclusively. Datetime strings must be formatted 
        to be compatible with Numpy datetime64, such as:
        "YYYY-MM-DD HH:MM:SS".

        start   : start datetime string.
        end     : optional datetime string, defaults to start.
        '''
        dates = self.all_dates()
        if end == '': end = start
        start = np.datetime64(start)
        end = np.datetime64(end)
        if end < start: 
            raise ValueError('The end time cannot be before you start')
        return self.table.where((dates >= start) & (dates <= end))

    def insert_modified_julian_day_column(self):
        " Creates and fills the ModifiedJD column. "
        self.table.add_column('ModifiedJD', self.__fill_JD(), dtype='float')

    def __fill_JD(self):
        " Fills the ModifiedJD column "
        f = lambda x: self.__mjd(x)
        return self.fill_column_by_function(f)
        
    def __mjd(self, comp):
        return self.modified_julian_day(np.datetime64(comp['Date_Time']))

    def fill_column_by_function(self, func):
        ''' 
        Uses a lambda function to generate contents for a column.
        Returns a list of the generated values.
        '''
        stack = []
        for row in self.table:
            stack.append(func(row))
        return stack

    def modified_julian_day(self, dt):
        ''' 
        Converts a numpy datetime to a float of the number of 
        modified Julian days. 
        '''
        delta = (dt - np.datetime64('1858-11-17 00:00'))
        days = delta.item().days
        secs = delta.item().seconds / (24.0 * 3600)
        return days + secs
        
        
        