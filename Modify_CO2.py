#!/usr/bin/env python

import numpy as np
import xarray as xr
import shutil
from matplotlib import pyplot as plt

# define file name
orgco2_file = '/cluster/shared/noresm/inputdata/atm/datm7/CO2/fco2_datm_global_simyr_1750-2014_CMIP6_c180929.nc'
newco2_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/fco2_datm_global_simyr_1750-2014_CMIP6_ESM2025.nc'

# copy file
shutil.copy(orgco2_file, newco2_file)

# Load the NetCDF file
ds = xr.open_dataset(newco2_file, decode_times=False)

# Load the TXT file
txt_file = '../From_Spirit/co2/co2_historical_annual_1850_2014.txt'
with open(txt_file) as f:
    co2_values = np.loadtxt(f)

# Store old CO2 values (for plotting comparison)
ds_old = ds.squeeze()

# Overvrite CO2
ds['CO2'][100:,0,0] = (co2_values[:,1])

# Create a new figure and axis
fig, ax = plt.subplots()

# Plot the old CO2 values as a blue line
ax.plot(np.arange(1750, 2015), ds_old['CO2'], color='blue', label='Old CO2')

# Plot the new CO2 values as a red line
ax.plot(np.arange(1750, 2015), ds['CO2'][:,0,0], color='red', label='New CO2')

# Add labels and legend
ax.set_xlabel('Year')
ax.set_ylabel('CO2 (ppm)')
ax.set_title('Comparison of old and new CO2 time series')
ax.legend()

# Save the plot
fig.savefig('Figures/Co2_plot.png')

# Save the modified NetCDF file
ds.to_netcdf(newco2_file)