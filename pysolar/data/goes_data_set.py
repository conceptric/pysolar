import os
from pysolar.data.data_set import DataSet
from pysolar.data.goes_file import *

class GoesDataSet(DataSet):
    '''
    Class to compile a series of GOES X-Ray data files into
    a dataset that can be manipulated by its methods.
    
    datafiles: a list of the file object in the dataset.
    '''    
    def __init__(self, filetype='xray'):
        super(GoesDataSet, self).__init__()
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
                
                