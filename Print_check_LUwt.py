#!/usr/bin/env python

import numpy as np
import xarray as xr
import netCDF4 as nc
import os

# define file names
surf_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc'
lu_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc'
#surf_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc_org'
# load the dataset

#using nc
#ds_surf = nc.Dataset(surf_file, mode='r')
#pct_crop = ds_surf['PCT_CROP'][:]    
#pct_natveg = ds_surf['PCT_NATVEG'][:]    
#pct_lake = ds_surf['PCT_LAKE'][:]  
#pct_glacier = ds_surf['PCT_GLACIER'][:]  
#pct_urban = ds_surf['PCT_URBAN'][:]  
#pct_nat_pft = ds_surf['PCT_NAT_PFT'][:]
#pct_cft = ds_surf['PCT_CFT'][:]

#using xr
ds_surf = xr.open_dataset(surf_file, mode='r')
pct_crop = ds_surf['PCT_CROP'].values
pct_natveg = ds_surf['PCT_NATVEG'].values
pct_lake = ds_surf['PCT_LAKE'].values
pct_glacier = ds_surf['PCT_GLACIER'].values
pct_urban = ds_surf['PCT_URBAN'].values
pct_nat_pft = ds_surf['PCT_NAT_PFT'].values
pct_cft = ds_surf['PCT_CFT'].values

sum_urb = np.sum(pct_urban, axis=0)
pct_all=pct_crop+pct_natveg + pct_lake + pct_glacier + sum_urb

limit=100.0000000000001
np.set_printoptions(precision=20)

#Check for values outside range
maskAbove = pct_all > limit
maskBelow = pct_all < 0.
print('here')
print(pct_all[maskAbove])
print(pct_all[maskBelow])

#Check for values outside range
maskAbove = pct_natveg > limit
maskBelow = pct_natveg < 0.
print('Check pct_natveg>100 or pct_natveg<0)')
print(pct_natveg[maskAbove])
print(pct_natveg[maskBelow])

#Check for values outside range
maskAbove = pct_crop > limit
maskBelow = pct_crop < 0.
print('Check pct_cft>100 or pct_cft<0)')
print(pct_crop[maskAbove])
print(pct_crop[maskBelow])

sum_pft = np.sum(pct_nat_pft, axis=0)
#Check for values outside range
maskAbove = sum_pft > limit
maskBelow = sum_pft < 0.
print('Check sum_pft>100 or sum_pft<0)')
print(sum_pft[maskAbove])
print(sum_pft[maskBelow])

sum_cft = np.sum(pct_cft, axis=0)
#Check for values outside range
maskAbove = sum_cft > limit
maskBelow = sum_cft < 0.
print('Check sum_cft>100 or sum_cft<0)')
print(sum_cft[maskAbove])
print(sum_cft[maskBelow])

#Check LU dataset
ds_LU = xr.open_dataset(lu_file , mode='r')
pct_cropLU = ds_LU['PCT_CROP'].values
maskAbove = pct_cropLU > limit
maskBelow = pct_cropLU < 0.
print('Check pct_crop>100 or pct_crop<0) in LU dataset')
print(pct_cropLU[maskAbove])
print(pct_cropLU[maskBelow])

# Close files (if using nc, not xr)
#ds_surf.close()
#ds_LU.close()