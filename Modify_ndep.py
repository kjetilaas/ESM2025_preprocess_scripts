#!/usr/bin/env python

import numpy as np
import netCDF4 as nc
import os
import subprocess

# define file name
CLMndep_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/fndep_clm_hist_b.e21.BWHIST.f09_g17.CMIP6-historical-WACCM.ensmean_1849-2015_monthly_0.9x1.25_ESM2025.nc'
CLMndep1850_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/fndep_clm_hist_b.e21.BWHIST.f09_g17.CMIP6-historical-WACCM.ymonavg_1850-1869_monthly_0.9x1.25_ESM2025.nc'
isimipndep_file_ =  os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/ndep_isimip_0.9x1.25_1850_2021_days.nc'

# copy and remap files with separate shell scrip
subprocess.call("./CopyAndRemapNDEP.sh", shell=True) 

# Load the NetCDF file
ds_CLM = nc.Dataset(CLMndep_file, mode='r+')
ds_CLM1850 = nc.Dataset(CLMndep_file, mode='r+')
ds_isimip = nc.Dataset(isimipndep_file_, mode='r')

sprmon = np.array((ds_isimip['time'][1:]-ds_isimip['time'][0:-1]) *60*60*24)
sprmon = np.append(sprmon,sprmon[0])

ndep_isimip = (ds_isimip['noy'][:] + ds_isimip['nhx'][:]) / np.broadcast_to(sprmon[:,np.newaxis,np.newaxis], ds_isimip['noy'].shape)

# update CLM ndep
print('Isimip ndep shape')
print(ndep_isimip.shape)
print('CLM ndep shape')
print(ds_CLM['NDEP_month'].shape)

#Duplicate first isimip year (for 1849) and replace 1850-2015
ds_CLM['NDEP_month'][:] = np.concatenate((ndep_isimip[0:12,:,:], ndep_isimip[0:1992,:,:]), axis=0)

print('CLM ndep shape after replacing with isimip')
print(ds_CLM['NDEP_month'].shape)

# set other variables to zero
ds_CLM['dry_deposition_NOy_as_N'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.
ds_CLM['wet_deposition_NOy_as_N'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.
ds_CLM['dry_deposition_NHx_as_N'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.
ds_CLM['wet_deposition_NHx_as_N'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.
ds_CLM['NDEP_NHx_month'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.
ds_CLM['NDEP_NOy_month'][:] = np.zeros_like(ds_CLM['NDEP_month'][:])-9999.

# Close NetCDF files
ds_CLM.close()
ds_isimip.close()