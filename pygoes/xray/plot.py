import atpy
import numpy as np
import matplotlib.dates as pld

def plot_goes(paxis, gdata):
    ''' Plots the GOES X-Ray data on the specified axis.
    
        plotaxis : pyplot axis object
        gdata    : an instance of GoesFile
    '''
    paxis.plot_date(pld.date2num(gdata.datetime.astype(np.datetime64).astype(object)), 
        gdata['0.1-0.8 nanometer (W/m2)'], label='GOES-15', fmt='--') 
    paxis.set_ylabel("GOES-15 0.1 - 0.8 nanometer (W/m2)")