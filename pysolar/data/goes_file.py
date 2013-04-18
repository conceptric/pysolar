import atpy
from numpy import datetime64

from pysolar.utils.datetime import DateCompiler
from pysolar.data import DataFile


class GoesFile(DataFile):
    ''' 
    Class to represent a GOES data file using ATPy tables.
    
    On creation it reads the file data from the path, 
    sets meaningful names for existing table columns, 
    and inserts a new column populated with datetime strings
    generated from the components first 4 columns of the original file.
    
    These datetime strings can be used directly to instantiate
    NumPy datetime64 objects.
    
    path    : path to the data file.
    fields  : Optional dictionary of file field names.
    The table attribute contains the ATPy table instance.       
    '''
    def __init__(self, path, fields={'col1': 'year',
                                    'col2': 'month',
                                    'col3': 'day', 
                                    'col4': 'time',
                                    'col5': 'JD days',
                                    'col6': 'JD secs'}):   
        super(GoesFile, self).__init__(path, delimiter='\s', 
        header_start=None, data_start=2)
        self.column_map = fields              
        self.table.keep_columns(self.get_column_map().keys())
        self.__rename_columns()
        self.__insert_new_columns()
    
    def __rename_columns(self):
        " Renames the imported columns with something more descriptive "
        for k, v in self.get_column_map().iteritems():
            if (k in self.table.names):
                self.table.rename_column(k, v)        

    def __insert_new_columns(self):
        " Inserts columns for JD date and datetime"
        self.table.add_column('Date_Time', self.__fill_datetimes(), 
            dtype='str')
        self.table.add_column('ModifiedJD', self.__fill_JD(), 
            dtype='float')

    def __fill_datetimes(self):
        " Fills the datetime column "
        f = lambda x: DateCompiler().build_datetime(x)
        return self.fill_column_by_function(f)
        
    def __fill_JD(self):
        " Fills the ModifiedJD column "
        f = lambda x: DateCompiler().modified_julian_date(x)
        return self.fill_column_by_function(f)
        
    def get_column_map(self):
        return self.column_map
        

class XrayGoesFile(GoesFile):
    ''' 
    Class to represent an X-Ray GOES data file using ATPy tables.
    
    On creation it reads the file data from the path, 
    sets meaningful names for existing table columns, 
    and inserts a new column populated with datetime strings
    generated from the components first 4 columns of the original file.
    
    These datetime strings can be used directly to instantiate
    NumPy datetime64 objects.
    
    path: path to the data file.
    The table attribute contains the ATPy table instance.       
    '''
    def __init__(self, path):
        FIELDS =  { 'col1': 'year',
                    'col2': 'month',
                    'col3': 'day', 
                    'col4': 'time',
                    'col5': 'JD days',
                    'col6': 'JD secs',
                    'col7': '0.05-0.4 nanometer (W/m2)',
                    'col8': '0.1-0.8 nanometer (W/m2)' }
        super(XrayGoesFile, self).__init__(path, FIELDS)
        
    
class MagneticGoesFile(GoesFile):
    ''' 
    Class to represent an Magnetometry GOES data file using ATPy tables.
    
    On creation it reads the file data from the path, 
    sets meaningful names for existing table columns, 
    and inserts a new column populated with datetime strings
    generated from the components first 4 columns of the original file.
    
    These datetime strings can be used directly to instantiate
    NumPy datetime64 objects.
    
    path: path to the data file.
    The table attribute contains the ATPy table instance.       
    '''    
    def __init__(self, path):
        FIELDS =   {'col1': 'year',
                    'col2': 'month',
                    'col3': 'day', 
                    'col4': 'time',
                    'col5': 'JD days',
                    'col6': 'JD secs',
                    'col7': 'Hp (nT)',
                    'col8': 'He (nT)',
                    'col9': 'Hn (nT)',
                    'col10': 'Total Field (nT)'}
        super(MagneticGoesFile, self).__init__(path, FIELDS)

