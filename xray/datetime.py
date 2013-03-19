import numpy as np
import atpy

def extract_goes_datetimes(table):
    ''' Builds a list of numpy datetimes from individual date and time columns of an ATPy table
        year    : 4 character string (2013 for example)
        month   : 2 character string (02 for February for example)
        day     : 2 character string (28 for example)
        time    : 4 character string representing a 24 hour clock
        return  : a list of the numpy datetime64 objects built from the concat strings
    '''
    stack = []
    for year, month, day, time, signal in table:
        dtstr = year + '-' + month + '-' + day + ' ' + time[:2] + ':' + time[2:]
        stack.append(np.datetime64(dtstr))
    return stack

def format_goes_table(table):
    ''' Adds a datetime string column to the ATPy table and removes the individual date and time columns
    '''
    datetimes = extract_goes_datetimes(table)
    table.remove_columns(('col1','col2','col3', 'col4'))
    table.rename_column('col8', 'goes-15')
    table.add_column('datetime', np.asarray(datetimes), dtype='str', before='goes-15')
    return table
    
class DateCompiler():
    """ Class with methods to build datetime strings from 
        a dictionary containing components.
    """

    def build_datetime(self, comp):
        time = "%04i" % (comp['time'])
        dt = "%04i-%02i-%02i %s:%s" % (comp['year'], comp['month'], comp['day'],
                                    time[:2], time[2:])
        return dt