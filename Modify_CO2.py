#!/usr/bin/env python

import numpy as np
import xarray as xr
import shutil
import netCDF4 as nc
from matplotlib import pyplot as plt

# define file name
orgco2_file = '/cluster/shared/noresm/inputdata/atm/datm7/CO2/fco2_datm_global_simyr_1750-2014_CMIP6_c180929.nc'
newco2_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/fco2_datm_global_simyr_1750-2014_CMIP6_ESM2025.nc'

# copy file
shutil.copy(orgco2_file, newco2_file)

# Load the NetCDF file
ds_nc = nc.Dataset(newco2_file, mode='r+')

co2 = ds_nc.variables['CO2']

# Load the TXT file
txt_file = '../From_Spirit/co2/co2_historical_annual_1850_2014.txt'
with open(txt_file) as f:
    co2_isimip = np.loadtxt(f)

# Store old CO2 values (for plotting comparison)
co2_old = co2[:]

# Overvrite CO2
co2[100:,0,0] = (co2_isimip[:,1])

# Create a new figure and axis
fig, ax = plt.subplots()

# Plot the old CO2 values as a blue line
ax.plot(np.arange(1750, 2015), co2_old[:,0,0], color='blue', label='Old CO2 ')

# Plot the new CO2 values as a red line
ax.plot(np.arange(1750, 2015), co2[:,0,0], color='red', label='New CO2 ')

# Add labels and legend
ax.set_xlabel('Year')
ax.set_ylabel('CO2 (ppm)')
ax.set_title('Comparison of old and new CO2 time series')
ax.legend()

# Save the plot
fig.savefig('Figures/Co2_plot.png')

# Save the modified NetCDF file
ds_nc.close()