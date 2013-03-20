import numpy as np
import atpy
   
class DateCompiler:
    '''
    Class with methods to build datetime strings from 
    a dictionary containing components.
    '''

    def build_datetime(self, comp):
        time = "%04i" % (comp['time'])
        components = (comp['year'], comp['month'], comp['day'],
                      time[:2], time[2:])
        dt = "%04i-%02i-%02i %s:%s" % components
        return dt