#!/usr/bin/env python

import numpy as np
import xarray as xr
import netCDF4 as nc4
import subprocess
import os
import Plot_LU

from matplotlib import pyplot as plt

# copy and remap files with separate shell scrip, of not done already
subprocess.call("./CopyAndRemapLU.sh", shell=True)

# define file names
new_landuse_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc'
new_surface_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc'
isimip_LUtotals_file = '/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/landuse-totals_histsoc_1.9x2.5deg_annual_1850_2014.nc'

# load the dataset
ds_LU = xr.open_dataset(new_landuse_file, decode_times=False)
ds_surf = xr.open_dataset(new_surface_file, decode_times=False)
ds_isimip = xr.open_dataset(isimip_LUtotals_file, decode_times=False)

# plot Crop maps and data series 
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 0, 'Crop_maps' )
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 164, 'Crop_maps' )

# map isimip crop types to clm input data
# so far only using total crop area, so only need to modify PCT_CROP
ds_LUnew=ds_LU
ds_surfnew=ds_surf

#pct_cropSURF = ds_surfnew['PCT_CROP']   
#pct_cropLU = ds_LUnew['PCT_CROP']   

pct_cropISIMIP = ds_isimip['cropland_total']
pct_cropISIMIPNoNan = np.where(np.isnan(pct_cropISIMIP), 0, pct_cropISIMIP)

ds_surfnew['PCT_CROP'].values=pct_cropISIMIPNoNan[0,:,:] * 100 
ds_surfnew['PCT_NATVEG']=ds_surfnew['PCT_NATVEG']+ds_surf['PCT_CROP'].values-ds_surfnew['PCT_CROP'].values
ds_LUnew['PCT_CROP'][0:-1,:,:].values=pct_cropISIMIPNoNan * 100 
ds_LUnew['PCT_CROP'][-1,:,:]=ds_LUnew['PCT_CROP'][-2,:,:]

# Save the modified NetCDF file
ds_LUnew.to_netcdf(new_landuse_file)
ds_surfnew.to_netcdf(new_surface_file)

Plot_LU.plot_land_use_data(ds_LUnew, ds_isimip, 0, 'Crop_maps_AfterModify' )
Plot_LU.plot_land_use_data(ds_LUnew, ds_isimip, 164, 'Crop_maps_AfterModify' ) 