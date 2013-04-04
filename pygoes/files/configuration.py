import os

class Configuration:
    """
    This class defines the configuration options for 
    the Files package.
    """
    def __init__(self, args={}):
        self.__set_default_attr()
        for key in args.keys():
            setattr(self, key, args[key])

    def __set_default_attr(self):
        self.source = ''
        self.cache = os.getcwd()
        self.file_template = '%s'