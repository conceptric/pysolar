from datetime import date, timedelta

'''
Module for utilites and custom errors for the files package.
'''
def get_range_of_dates(start=None, finish=None):
    if start and finish:
        offset = range(0, ((finish - start).days + 1))
        return [ start + timedelta(days=x) for x in offset ]
    else:
        return []

def get_date_range_strings(start, finish, format='%Y%m%d'):
    date_range = get_range_of_dates(start, finish)
    return [ adate.strftime(format) for adate in date_range ]

class MissingFileError(Exception):
    """ An error for when a file could not be found. """
    pass

