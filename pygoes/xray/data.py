import atpy
from pygoes.xray.datetime import DateCompiler

class GoesFile():
    ''' 
    Class to represent a GOES-15 W-Ray data file using ATPy tables.
    
    On creation it reads the file data from the path, 
    sets meaningful names for existing table columns, 
    and inserts a new column populated with datetime strings
    generated from the components first 4 columns of the original file.
    
    These datetime strings can be used directly to instantiate
    NumPy datetime64 objects.
    
    Path: path to the data file.
    The table attribute contains the ATPy table instance.       

    '''
    
    columns = {'col1': 'year',
               'col2': 'month',
               'col3': 'day', 
               'col4': 'time',
               'col7': '0.05-0.4 nanometer (W/m2)',
               'col8': '0.1-0.8 nanometer (W/m2)'}
    
    def __init__(self, path):         
        self.table = self.__read(path)
        self.__rename_columns()
        self.__insert_datetime_column()
    
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

    def __insert_datetime_column(self):
        " Inserts a column for datetime"
        self.table.add_column('datetime', self.__fill_datetimes(), 
            dtype='str', after='time')

    def __fill_datetimes(self):
        " Fills the datetime column "
        stack = []
        for row in self.table:
            stack.append(DateCompiler().build_datetime(row))
        return stack