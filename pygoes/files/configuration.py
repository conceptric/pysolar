import os

class Configuration:
    """
    This class defines the configuration options for 
    the Files package.
    """
    def __init__(self, args={}):
        if 'source' in args.keys():
            self.source = args['source']
        else:
            self.source = ''
        if 'cache' in args.keys():
            self.cache = args['cache']
        else:
            self.cache = os.getcwd()
        if 'file_template' in args.keys():
            self.file_template = args['file_template']
        else:
            self.file_template = '%s'
