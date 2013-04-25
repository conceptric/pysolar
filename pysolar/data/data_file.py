import atpy
import numpy as np

from pysolar.utils.datetime import *


class DataTable(atpy.Table):
    """
    Class to extend the basic ATPy Table with a methods to 
    query and manipulate data containing DateTimes.
    
    Can be instantiated using all the normal ATPy Table methods.
    """
    datetime_label  = 'Date_Time'
    mjd_label       = 'ModifiedJD'
        
    def size(self):
        ' Returns an integer for the number of records '
        return len(self)

    def all_dates(self):
        ' Returns a numpy array containing all the datetimes '
        return self[self.datetime_label].astype(np.datetime64)

    def begins(self):
        ' Returns the earliest datetime in the file '
        return self.all_dates().min()

    def finishes(self):
        ' Returns the latest datetime in the file '
        return self.all_dates().max()

    def sort_by_mjd(self):
        ' Sorts the data records into datetime order '
        self.sort(self.mjd_label)

    def has_column(self, name):
        ' Returns True if present, and False if not '
        try:
            self[name]
            return True
        except ValueError:
            return False

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
        return self.where((dates >= start) & (dates <= end))
    

class DataFile(object):
    """
    Class to represent the contents of a data file and 
    provide basic methods to query and manipulate these 
    data using ATPy tables.
    
    path        : path to the data file.
    delimiter   : optional data delimiter, defaults to ",".
    header_start: optional position of header row, defaults to 0.
    data_start  : optional position of first data row, defaults to 1.
     
    The table attribute contains a DataTable instance, subclass of ATPy Table.           
    """
    def __init__(self, path, delimiter=',', header_start=0, data_start=1):
        self.table = self.__read(path, delimiter, header_start, data_start)
        if self.has_column(self.datetime_label):
            self.insert_modified_julian_day_column()            
    
    def __read(self, path, delimiter, header_start, data_start):
        data = DataTable(path, type="ascii", delimiter=delimiter, 
        header_start=header_start, data_start=data_start)
        return data

    def __getattr__(self, name):
        ' Forwards unknown attributes to the wrapped Table '
        return getattr(self.table, name)

    def insert_modified_julian_day_column(self):
        " Creates and fills the ModifiedJD column. "
        self.table.add_column(self.mjd_label, self.dates_as_mjd(), dtype='float')

    def dates_as_mjd(self):
        " Returns a list of Modified Julian Days corresponding to the Date_Time. "
        f = lambda x: modified_julian_day(np.datetime64(x[self.datetime_label]))
        return self.fill_column_by_function(f)
        
    def fill_column_by_function(self, func):
        ''' 
        Uses a lambda function to generate contents for a column.
        Returns a list of the generated values.
        '''
        stack = []
        for row in self.table:
            stack.append(func(row))
        return stack
       
                