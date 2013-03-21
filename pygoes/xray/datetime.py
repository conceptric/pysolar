import numpy as np
import atpy
   
class DateCompiler:
    '''
    Class with methods to build datetime strings from 
    a dictionary containing components.
    '''

    def build_datetime(self, comp):
        '''
        Generates a string for datetime from components in a dictionary
        including:
        year YYYY
        month MM
        day DD
        time 0000
        
        '''
        time = "%04i" % (comp['time'])
        components = (comp['year'], comp['month'], comp['day'],
                      time[:2], time[2:])
        dt = "%04i-%02i-%02i %s:%s" % components
        return dt
        
    def modified_julian_date(self, comp):
        '''
        Generated a 5 decimal place float of Julian Date
        from components for JD days and JD seconds.
        '''
        secs_per_day = 24 * 3600.0 
        time = comp['JD days'] + ( comp['JD secs'] / secs_per_day )
        return round(time, 5)