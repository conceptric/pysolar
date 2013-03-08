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
