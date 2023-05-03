#!/usr/bin/env python

import numpy as np
import netCDF4 as nc
import subprocess
import os
import Plot_LU
import Plot_Surf

from matplotlib import pyplot as plt

# copy and remap files with separate shell scrip
subprocess.call("./CopyAndRemapLU.sh", shell=True)

# define file names
new_landuse_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc'
new_surface_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc'
isimip_LUtotals_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/landuse-totals_histsoc_1.9x2.5deg_annual_1850_2014.nc'

# load the dataset
ds_LU = nc.Dataset(new_landuse_file, mode='r+')
ds_surf = nc.Dataset(new_surface_file, mode='r+')
ds_isimip = nc.Dataset(isimip_LUtotals_file, mode='r')

# plot Crop maps and data series 
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 0, 'Crop_maps' )
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 164, 'Crop_maps' )

# map isimip crop types to clm input data
# so far only using total crop area, so only need to modify PCT_CROP

frac_cropISIMIP = ds_isimip['cropland_total'][:]
frac_cropISIMIP = np.where(frac_cropISIMIP>1., 0, frac_cropISIMIP)
frac_cropISIMIP = np.where(frac_cropISIMIP<0., 0, frac_cropISIMIP)

pct_crop = ds_surf['PCT_CROP'][:]    
pct_natveg = ds_surf['PCT_NATVEG'][:]    
pct_lake = ds_surf['PCT_LAKE'][:]  
pct_glacier = ds_surf['PCT_GLACIER'][:]  
pct_urban = ds_surf['PCT_URBAN'][:]  
sum_urb = np.sum(pct_urban, axis=0)
sum_all = pct_natveg + pct_crop + pct_lake + pct_glacier + sum_urb
pct_natcrop = pct_natveg + pct_crop
# overwrite pct_crop, only where original file had nat+crop>0
pct_cropnew = frac_cropISIMIP[0,:,:] * 100
pct_cropnew = np.where(pct_natcrop>=pct_cropnew, pct_cropnew, pct_crop)
ds_surf['PCT_CROP'][:] = pct_cropnew
# update pct_natveg, consistent with all pct
ds_surf['PCT_NATVEG'][:] =  sum_all - pct_cropnew - pct_lake - pct_glacier - sum_urb

# update landuse timeseries
pct_cropLU = ds_LU['PCT_CROP'][:]    
pct_cropnewLU = frac_cropISIMIP * 100 
pct_cropnewLU = np.where(pct_natcrop>=pct_cropnewLU, pct_cropnewLU, pct_cropLU[-1,:,:])
ds_LU['PCT_CROP'][0:-1,:,:]=pct_cropnewLU
ds_LU['PCT_CROP'][-1,:,:]=ds_LU['PCT_CROP'][-2,:,:]

# Plot modified files
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 0, 'Crop_maps_AfterModify' )
Plot_LU.plot_land_use_data(ds_LU, ds_isimip, 164, 'Crop_maps_AfterModify' ) 

Plot_Surf.plot_surface(ds_surf,'Surf_AfterModify')

# Save the modified NetCDF file
ds_LU.close()
ds_surf.close()