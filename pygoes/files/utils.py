'''
Module for custom errors relevant to the files package.
'''
class MissingFileError(Exception):
    """ An error for when a file could not be found. """
    pass
