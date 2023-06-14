#!/usr/bin/env python

import numpy as np
import netCDF4 as nc
import os
import subprocess

# define file name
CLMndep_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/fndep_clm_f09_g17.CMIP6-SSP1-2.6-WACCM_1849-2101_monthly_ESM2025.nc'
isimipndep_file_ =  os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/ndep_isimip_ssp126_0.9x1.25_2015_2100_days.nc'

# copy and remap files with separate shell scrip
subprocess.call("./CopyAndRemapNDEP_ssp126.sh", shell=True) 

# Load the NetCDF file
ds_CLM = nc.Dataset(CLMndep_file, mode='r+')
ds_isimip = nc.Dataset(isimipndep_file_, mode='r')

sprmon = np.array((ds_isimip['time'][1:]-ds_isimip['time'][0:-1]) *60*60*24)
sprmon = np.append(sprmon,sprmon[0])

ndep_isimip = (ds_isimip['noy'][:] + ds_isimip['nhx'][:]) / np.broadcast_to(sprmon[:,np.newaxis,np.newaxis], ds_isimip['noy'].shape)
ndep_org = ds_CLM['NDEP_month'][:]

# update CLM ndep
print('Isimip ndep shape')
print(ndep_isimip.shape)
print('CLM ndep shape')
print(ds_CLM['NDEP_month'].shape)

#Replace years 2015-2100, duplucate yr 2100 (to 2101) and keep years 1849-2014
ds_CLM['NDEP_month'][:] = np.concatenate((ndep_org[0:1992,:,:], ndep_isimip[0:1032,:,:], ndep_isimip[1020:1032,:,:]), axis=0)

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