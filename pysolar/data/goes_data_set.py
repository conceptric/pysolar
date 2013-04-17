import os
from pysolar.data.goes_file import *

class GoesDataSet:
    '''
    Class to compile a series of GOES X-Ray data files into
    a dataset that can be manipulated by its methods
    
    datafiles: a list of the file object in the dataset
    '''    
    
    def __init__(self, filetype='xray'):
        self.datafiles = []
        self.filetype = filetype
        
    def compile(self, root_path, files):
        '''
        Imports the data files as GoesFile instances
        
        root_path = path to the base file directory
        files     = a list of the filename strings to import
        '''
        for file in files:
            try:
                if self.filetype == 'magnetic':
                    datafile = MagneticGoesFile(os.path.join(root_path, file))                    
                else:
                    datafile = XrayGoesFile(os.path.join(root_path, file))                    
                self.datafiles.append(datafile)
            except IOError:
                pass
        
    def select_between_dates(self, start, end):
        ''' 
        Returns a table containing records between, and inclusive of, 
        the datetimes defined by the provided strings formatted:
        
        "YYYY-MM-DD HH:MM:SS"
        
        start   = first datetime to be retrieved
        end     = last datetime to be retrieved
        '''
        query = []
        for file in self.datafiles:
            query.append(file.select_between_dates(start, end))
        return self.__combine_tables(query)
        
    def __combine_tables(self, tables):
        table = tables[0]
        for i in range(1, len(tables), 1):
            table.append(tables[i])
        table.sort('ModifiedJD')
        return table
        
                
