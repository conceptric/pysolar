''' Library of functions to manipulate GOES-15 X-Ray data files.  

Modules included are:
data: tools to import goes files.
datetime: tools to extract and work with dates and times.
plot: tools to help plot these data.

'''
from data import *
from datetime import *
from plot import *

__all__ = ["data", "datetime", "plot"]