import atpy
from pysolar.utils.datetime import DateCompiler
from numpy import datetime64

XRAY_FIELDS =  {'col1': 'year',
                'col2': 'month',
                'col3': 'day', 
                'col4': 'time',
                'col5': 'JD days',
                'col6': 'JD secs',
                'col7': '0.05-0.4 nanometer (W/m2)',
                'col8': '0.1-0.8 nanometer (W/m2)'}

MAG_FIELDS =   {'col1': 'year',
                'col2': 'month',
                'col3': 'day', 
                'col4': 'time',
                'col5': 'JD days',
                'col6': 'JD secs',
                'col7': 'Hp (nT)',
                'col8': 'He (nT)',
                'col9': 'Hn (nT)',
                'col10': 'Total Field (nT)'}

class GoesFile:
    ''' 
    Class to represent a GOES data file using ATPy tables.
    
    On creation it reads the file data from the path, 
    sets meaningful names for existing table columns, 
    and inserts a new column populated with datetime strings
    generated from the components first 4 columns of the original file.
    
    These datetime strings can be used directly to instantiate
    NumPy datetime64 objects.
    
    Path: path to the data file.
    The table attribute contains the ATPy table instance.       

    '''
    def __init__(self, path, filetype='xray'):         
        if filetype == 'magnetic':
            self.column_map = MAG_FIELDS
        else:
            self.column_map = XRAY_FIELDS        
        
        self.table = self.__read(path)
        self.__rename_columns()
        self.__insert_new_columns()
    
    def __read(self, path):
        goes = atpy.Table(path, type="ascii", delimiter="\s", 
            header_start=None, data_start=2)
        goes.keep_columns(self.get_column_map().keys())
        return goes
        
    def __rename_columns(self):
        " Renames the imported columns with something more descriptive "
        for k, v in self.get_column_map().iteritems():
            if (k in self.table.names):
                self.table.rename_column(k, v)        

    def __insert_new_columns(self):
        " Inserts columns for JD date and datetime"
        self.table.add_column('datetime', self.__fill_datetimes(), 
            dtype='str')
        self.table.add_column('Modified JD', self.__fill_JD(), 
            dtype='float')

    def __fill_datetimes(self):
        " Fills the datetime column "
        f = lambda x: DateCompiler().build_datetime(x)
        return self.__fill_column(f)
        
    def __fill_JD(self):
        " Fills the Modified JD column "
        f = lambda x: DateCompiler().modified_julian_date(x)
        return self.__fill_column(f)
        
    def __fill_column(self, func):
        stack = []
        for row in self.table:
            stack.append(func(row))
        return stack

    def get_column_map(self):
        return self.column_map

    def get_date_range(self, start, end):
        ''' 
        Returns a table containing records between, and inclusive of, 
        the datetimes defined by the provided strings formatted:
        
        "YYYY-MM-DD HH:MM:SS"
        
        start   = first datetime to be retrieved
        end     = last datetime to be retrieved
        '''
        start_time = datetime64(start)
        end_time = datetime64(end)
        if end_time < start_time: 
            raise ValueError('The end time cannot be before you start')
        
        datetimes = self.table.datetime.astype(datetime64)
        
        query = self.table.where(
         (datetimes >= start_time) & (datetimes <= end_time))
        return query
        


