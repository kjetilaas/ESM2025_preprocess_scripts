#!/usr/bin/env python

import numpy as np
import xarray as xr
import shutil
import netCDF4 as nc
from matplotlib import pyplot as plt

# define file name
orgpop_file = '/cluster/shared/noresm/inputdata/lnd/clm2/firedata/clmforc.Li_2017_HYDEv3.2_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2016_c180202.nc'
static_file = '/cluster/shared/noresm/inputdata/lnd/clm2/surfdata_map/surfdata_360x720cru_16pfts_CMIP6_simyr2000_c170706.nc'
isimip_file = '/cluster/shared/noresm/isimip_data/population/population_histsoc_30arcmin_annual_1901_2014.nc'
# this sould be moved into somewhere shared
isimip2_file = '/cluster/home/kjetisaa/ESM2025_input/Div_files/population_histsoc_30arcmin_annual_1901_2020.nc'
# copy file
#shutil.copy(orgpop_file, newpop_file)

# Load the NetCDF file
dspop_nc = nc.Dataset(orgpop_file, mode='r')
dssurf_nc = nc.Dataset(static_file, mode='r')
dsismip_nc = nc.Dataset(isimip_file, mode='r')
dsismip2_nc = nc.Dataset(isimip2_file, mode='r')

area = dssurf_nc['AREA'][:]
popdensCLM = dspop_nc['hdm'][:]
popHYDE33 = dsismip_nc['total-population'][:]
popHYDE32 = dsismip2_nc['popc'][:]

#totpopCLM = np.sum(popdensCLM*area, axis=(1,2)) #should this be scaled with land fraction?
totpopHYDE33 = np.sum(popHYDE33, axis=(1,2))
totpopHYDE32 = np.sum(popHYDE32, axis=(1,2))

print(popdensCLM.shape)
print(totpopCLM.shape)
print(totpopHYDE33.shape)

# Create a new figure and axis
fig, ax = plt.subplots()

# Plot CLM population
#ax.plot(np.arange(1850, 2017), totpopCLM, color='blue', label='CLM pop')

# Plot HYDE3.3 population
ax.plot(np.arange(1901, 2015), totpopHYDE33, color='red', label='ISIMIP3 pop')

# Plot HYDE3.2 population
ax.plot(np.arange(1901, 2021), totpopHYDE32, color='green', label='ISIMIP2 pop')

# Add labels and legend
ax.set_xlabel('Year')
ax.set_ylabel('Total population')
ax.set_title('Comparison of ISIMIP2 and ISIMIP3 populations')
ax.legend()
plt.grid()

# Save the plot
fig.savefig('Figures/Population_check.png')

# Close NetCDF files
dspop_nc.close()
dssurf_nc.close()
dsismip_nc.close()