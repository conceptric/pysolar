import numpy as np
import atpy

SECONDS_PER_DAY = (24.0 * 3600)
MJD_BASELINE = np.datetime64('1858-11-17 00:00')

def modified_julian_day(dt):
    ''' 
    Returns the datetime as modified Julian days 
    rounded to 5 decimal places. 
    '''
    delta = (dt - MJD_BASELINE)
    days = delta.item().days
    secs = delta.item().seconds / SECONDS_PER_DAY
    return round(days + secs, 5)

   
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