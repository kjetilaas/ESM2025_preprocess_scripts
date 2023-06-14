#!/usr/bin/env python

import numpy as np
import netCDF4 as nc
import subprocess
import os
import Plot_LU

from matplotlib import pyplot as plt

# define scenario and experiment
ssp_name1 = 'ssp370' #ssp126, ssp370
ssp_name2 = 'SSP3-7.0' # SSP1-2.6, SSP3-7.0

exp_name = 'agtonat' # noluc, agtonat, agtoaff, nattoaff, agtobio, nattobio
# define file names
org_landuse_file = '/cluster/shared/noresm/inputdata/lnd/clm2/surfdata_map/release-clm5.0.18/landuse.timeseries_1.9x2.5_' + ssp_name2 + '_78pfts_CMIP6_simyr1850-2100_c190228.nc'
new_landuse_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_' + ssp_name2 + '_78pfts_CMIP6_simyr1850-2100_ESM2025_' + exp_name + '.nc'
hist_landuse_file = os.environ.get('USERWORK')+'/isimip_forc/Ohter_modified_files/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc'
history_file = os.environ.get('USERWORK')+'/archive/ESM2025_UKESM1-0-LL_BGC-CROP_HIST_f19_g17_historical/lnd/hist/ESM2025_UKESM1-0-LL_BGC-CROP_HIST_f19_g17_historical.clm2.h0.2014-12.nc'

print(ssp_name1)
print(org_landuse_file)
print(new_landuse_file)
print(hist_landuse_file)

# copy file
subprocess.run(['cp', org_landuse_file, new_landuse_file])

# load the dataset
ds_LU = nc.Dataset(new_landuse_file, mode='r+')
ds_LU_hist = nc.Dataset(hist_landuse_file, mode='r')
ds_history = nc.Dataset(history_file, mode='r')


# overwrite historical period
ds_LU['PCT_CROP'][0:166,:,:]=ds_LU_hist['PCT_CROP'][0:166,:,:]

# make transition in 2015 (experiment)
natpft_2015 = ds_LU['PCT_NAT_PFT'][165:166, :, :, :]
pctcrop_2015 = ds_LU['PCT_CROP'][165:166, :, :]
pctcft_2015 = ds_LU['PCT_CFT'][165:166, :, :, :]

pct_natveg = ds_history['PCT_LANDUNIT'][0,0, :, :]
pct_grass = np.sum(natpft_2015[0,12:15,:,:], axis=0)
pct_forest = np.sum(natpft_2015[0,1:9,:,:], axis=0)
pct_nonforest = np.sum(natpft_2015[0,9:15,:,:], axis=0) + natpft_2015[0,0,:,:]

print(pct_natveg.shape)
print(pct_forest.shape)
print(pct_nonforest.shape)
print(natpft_2015.shape)

if exp_name == 'noluc':
    print('noluc')
elif exp_name == 'agtonat': #Conversion of agricultural land to natural land
    print('agtonat') 
    # change pct_crop (implicitly changing pct_natveg), keeping pft and cft distributions
    pctcrop_2015 = np.where(pctcrop_2015>5.0,pctcrop_2015 - 5.0, pctcrop_2015)    
elif exp_name == 'agtoaff': #Conversion of agricultural land to afforestation
    print('agtoaff')
    # create new pft distribution 
    # demand at least 5% forest in grid cell before transition
    # don't change distribution where forest already dominates (but still do crop->natveg)
    
    addforest=5*100/pct_natveg

    natpft_2015[0,0,:,:] = np.where((pctcrop_2015>5.0) & (pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest), natpft_2015[0,0,:,:] - addforest*(natpft_2015[0,0,:,:]/pct_nonforest), natpft_2015[0,0,:,:])
    for i in range(1, 9):
        natpft_2015[0,i,:,:] = np.where((pctcrop_2015>5.0) & (pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest),natpft_2015[0,i,:,:] + addforest*(natpft_2015[0,i,:,:]/pct_forest), natpft_2015[0,i,:,:])
    for i in range(9,15):
        natpft_2015[0,i,:,:] = np.where((pctcrop_2015>5.0) & (pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest),natpft_2015[0,i,:,:] - addforest*(natpft_2015[0,i,:,:]/pct_nonforest), natpft_2015[0,i,:,:])

    # reduce crop area with 5 pct
    pctcrop_2015 = np.where((pctcrop_2015>5.0) & (pct_forest>5.0),pctcrop_2015 - 5.0, pctcrop_2015)  

elif exp_name == 'nattoaff': #Conversion of natural land to afforestation
    print('nattoaff')
    # create new pft distribution 
    # demand at least 5% forest in grid cell before transition (don't plant trees where they cannot live)
    # don't change distribution where forest already dominates (only do transitions of full 5% of grid cell)
    
    addforest=5*100/pct_natveg

    natpft_2015[0,0,:,:] = np.where((pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest), natpft_2015[0,0,:,:] - addforest*(natpft_2015[0,0,:,:]/pct_nonforest), natpft_2015[0,0,:,:])
    for i in range(1, 9):
        natpft_2015[0,i,:,:] = np.where((pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest),natpft_2015[0,i,:,:] + addforest*(natpft_2015[0,i,:,:]/pct_forest), natpft_2015[0,i,:,:])
    for i in range(9,15):
        natpft_2015[0,i,:,:] = np.where((pct_forest>5.0) & (pct_forest<addforest) & (pct_nonforest>addforest),natpft_2015[0,i,:,:] - addforest*(natpft_2015[0,i,:,:]/pct_nonforest), natpft_2015[0,i,:,:])

elif exp_name == 'agtobio': #Conversion of agricultural land to bioenergy
    print('agtobio')
    addbio = 5*100/pctcrop_2015
    
    print(pctcrop_2015.shape)
    print(pctcft_2015.shape)
    

   # subtract area from all (other) cfts
    for i in range(0, 64):
        print('i='+str(i))    
        pctcft_2015[0,i,:,:] = np.where((pctcrop_2015>5.0) ,pctcft_2015[0,i,:,:] - addbio*(pctcft_2015[0,i,:,:]/100), pctcft_2015[0,i,:,:])

    # add area to rainfed switchgrass
    i=72-14
    print('i='+str(i))    
    pctcft_2015[0,i,:,:] = np.where((pctcrop_2015>5.0) ,pctcft_2015[0,i,:,:] + addbio, pctcft_2015[0,i,:,:])

elif exp_name == 'nattobio': #Conversion of natural land to bioenergy. Do for all forested land. Keep PFT dist    
    print('nattobio')
    print('Not implemented')


else: 
    print('No exp_name match')
    print('will use noluc')


#check new distribution
print('Checking new natpft distribution (should be 100, 100, =<100, >=0)')
print(np.max(np.max(np.sum(natpft_2015[0,:,:,:],axis=0))))
print(np.min(np.min(np.sum(natpft_2015[0,:,:,:],axis=0))))
print(np.max(np.max(np.max(natpft_2015[0,:,:,:]))))
print(np.min(np.min(np.min(natpft_2015[0,:,:,:]))))

print('Checking new cft distribution (should be 100, 100, =<100, >=0)')
print(np.max(np.max(np.sum(pctcft_2015[0,:,:,:],axis=0))))
print(np.min(np.min(np.sum(pctcft_2015[0,:,:,:],axis=0))))
print(np.max(np.max(np.max(pctcft_2015[0,:,:,:]))))
print(np.min(np.min(np.min(pctcft_2015[0,:,:,:]))))

# broadcast 2015 to 2016-2100
broadcasted_values_natpft = np.broadcast_to(natpft_2015, (251-165, ) + natpft_2015.shape[1:])
ds_LU['PCT_NAT_PFT'][165:, :, :, :] = broadcasted_values_natpft

broadcasted_values_pctcrop = np.broadcast_to(pctcrop_2015, (251-165, ) + pctcrop_2015.shape[1:])
ds_LU['PCT_CROP'][165:, :, :] = broadcasted_values_pctcrop

broadcasted_values_pctcft = np.broadcast_to(pctcft_2015, (251-165, ) + pctcft_2015.shape[1:])
ds_LU['PCT_CFT'][165:, :, :, :] = broadcasted_values_pctcft

Plot_LU.plot_land_use_data2(ds_LU, ds_LU_hist, 165, 'Crop_maps_' + exp_name ) 
#Plot_LU.plot_forest(ds_LU, 165, 'Forest_maps_' + exp_name )

# Save the modified NetCDF file
ds_LU.close()
ds_LU_hist.close()