#!/usr/bin/env python

import numpy as np
import xarray as xr
import netCDF4 as nc
import subprocess
import os
import Plot_LU

from matplotlib import pyplot as plt

# copy and remap files with separate shell scrip
subprocess.call("./CopyAndRemapLU.sh", shell=True)

# define file names
new_landuse_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc'
new_surface_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc'
isimip_LUtotals_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/landuse-totals_histsoc_1.9x2.5deg_annual_1850_2014.nc'

# load the dataset
ds_LU = nc.Dataset(new_landuse_file, mode='r+')
ds_surf = nc.Dataset(new_surface_file, mode='r+')
ds_isimip = nc.Dataset(isimip_LUtotals_file, mode='r')

# plot Crop maps and data series 
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 0, 'Crop_maps' )
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 164, 'Crop_maps' )

# map isimip crop types to clm input data
# so far only using total crop area, so only need to modify PCT_CROP

ds_LUnew=ds_LU
pct_crop_old=ds_surf['PCT_CROP'][:]

pct_cropISIMIP = ds_isimip['cropland_total'][:]
pct_cropISIMIPNoNan = np.where(pct_cropISIMIP>1., 0, pct_cropISIMIP)

ds_surf['PCT_CROP'][:]=pct_cropISIMIPNoNan[0,:,:] * 100 
ds_surf['PCT_NATVEG'][:]=ds_surf['PCT_NATVEG']+pct_crop_old-ds_surf['PCT_CROP'][:]
ds_LU['PCT_CROP'][0:-1,:,:].values=pct_cropISIMIPNoNan * 100 
ds_LU['PCT_CROP'][-1,:,:]=ds_LU['PCT_CROP'][-2,:,:]

# Plot modified files
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 0, 'Crop_maps_AfterModify' )
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 164, 'Crop_maps_AfterModify' ) 

# Save the modified NetCDF file
ds_LU.close()
ds_surf.close()