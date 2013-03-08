import atpy
import numpy as np
import matplotlib.dates as pld

def plot_goes(plotaxis, goes, datemin, datemax):
    ''' Plots the GOES X-Ray data for a defined time range on the specified axis
        plotaxis: pyplot axis object
        goes    : formatted GOES datetime and xray flux data table
        datemin : Numpy datetime64 of the start time
        datemax : Numpy datetime64 of the end time
    '''
    pgoes = goes.where((goes.datetime.astype(np.datetime64) >= datemin) & (goes.datetime.astype(np.datetime64) <= datemax))
    plotaxis.plot_date(pld.date2num(pgoes.datetime.astype(np.datetime64).astype(object)), pgoes['goes-15'], label='goes-15', fmt='--') 
    plotaxis.set_ylabel("GOES-15 0.1 - 0.8 nanometer (W/m2)")