import atpy
import asciitable

def read(path):
    ''' Imports the specified GOES X-Ray data file and returns the required data columns as an ATPy table
        path    : a string containing the path to the file
        returns : an ATPy table containing columns for the component of datetime 
                  and 0.1 - 0.8 nanometer x-ray data as strings.
    '''
    converters = {'col1': [asciitable.convert_list(str)],
                  'col2': [asciitable.convert_list(str)],
                  'col3': [asciitable.convert_list(str)],
                  'col4': [asciitable.convert_list(str)]}
    goes = atpy.Table(path, type="ascii", delimiter="\s", header_start=None, data_start=2, converters=converters)
    goes.keep_columns(('col1','col2','col3', 'col4', 'col8'))
    return goes

class GoesFile():
    ''' Class to represent a GOES-15 W-Ray data file using ATPy 
        Path: path to the data file
    '''
    
    columns = {'col1': 'year',
               'col2': 'month',
               'col3': 'day', 
               'col4': 'time',
               'col7': '0.05- 0.4 nanometer (W/m2)',
               'col8': '0.1 - 0.8 nanometer (W/m2)'}
    
    def __init__(self, path):
        " Reads the file data and sets table column names "
        self.table = self.__read(path)
        self.__rename_columns()
    
    def __read(self, path):
        goes = atpy.Table(path, type="ascii", delimiter="\s", 
            header_start=None, data_start=2)
        goes.keep_columns(self.columns.keys())
        return goes
        
    def __rename_columns(self):
        " Renames the imported columns with something more descriptive "
        for k, v in self.columns.iteritems():
            if (k in self.table.names):
                self.table.rename_column(k, v)        
                