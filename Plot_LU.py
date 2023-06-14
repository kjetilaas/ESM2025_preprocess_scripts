import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def plot_land_use_data(ds1, ds2, t, figname_in):
    filename='Figures/' + figname_in + '_' + str(1850+t) +  '.png'
    # CLM LU data
    pct_crop1 = ds1['PCT_CROP'][:]    
    lat1 = ds1['LATIXY'][:]
    lon1 = ds1['LONGXY'][:]
    area = ds1['AREA'][:]
    # Isimip LU data    
    pct_crop2 = ds2['cropland_total'][:] * 100.  
    lat2 = ds2['lat'][:]
    lon2 = ds2['lon'][:]

    # Create figure
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12), subplot_kw={'projection': 'rectilinear'})
    fig.suptitle('Land Use Data, year' + str(1850+t))

    # Plot pct_crop on top left subplot
    im1 = axs[0, 0].pcolormesh(lon1, lat1, pct_crop1[t,:,:], cmap='YlGn', vmin=0, vmax=100)
    axs[0, 0].set_title('PCT_CROP CLM LU file')
    fig.colorbar(im1, ax=axs[0, 0])

    # Plot pct_crop from LU file on top right subplot
    im2 = axs[0, 1].pcolormesh(lon2, lat2, pct_crop2[t,:,:], cmap='YlGn', vmin=0, vmax=100)
    #ax2.set_title('PCT_CROP LU file, time='+ str(t))
    axs[0, 1].set_title('PCT_CROP ISIMIP file')
    fig.colorbar(im2, ax=axs[0, 1])

    # Plot difference on lower left subplot
    im3 = axs[1, 0].pcolormesh(lon1, lat1, pct_crop2[t,:,:]-pct_crop1[t,:,:], cmap='RdBu_r', vmin=-10, vmax=10)
    axs[1, 0].set_title('Difference (ISIMIP-Default)')
    fig.colorbar(im3, ax=axs[1, 0])

    #Plot time series of area-weighted pct_crop on bottom right subplot
    area_broadcast1 = np.broadcast_to(area, pct_crop1.shape)
    area_broadcast2 = np.broadcast_to(area, pct_crop2.shape)

    pct_crop1_wt = (pct_crop1 * area_broadcast1)
    pct_crop2_wt = (pct_crop2 * area_broadcast2)

    axs[1, 1].plot(np.arange(1850, 2016),np.sum(pct_crop1_wt, axis=(1,2)), label='CLM LU file')
    axs[1, 1].plot(np.arange(1850, 2015),np.sum(pct_crop2_wt, axis=(1,2)), label='ISIMIP file')
    axs[1, 1].set_title('Area-weighted PCT_CROP time series')
    axs[1, 1].legend()

    # Adjust subplots and save figure
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(filename)

    return fig


def plot_land_use_data2(ds1, ds2, t, figname_in):
    filename='Figures/' + figname_in + '_' + str(1850+t) +  '.png'
    # CLM LU data
    pct_crop1 = ds1['PCT_CROP'][:]    
    lat1 = ds1['LATIXY'][:]
    lon1 = ds1['LONGXY'][:]
    area = ds1['AREA'][:]

    # Isimip LU data    
    pct_crop2 = ds2['PCT_CROP'][:]  
    lat2 = ds2['LATIXY'][:]
    lon2 = ds2['LONGXY'][:]

    # Create figure
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12), subplot_kw={'projection': 'rectilinear'})
    fig.suptitle('Land Use Data, year' + str(1850+t))

    # Plot pct_crop on top left subplot
    im1 = axs[0, 0].pcolormesh(lon1, lat1, pct_crop1[t,:,:], cmap='YlGn', vmin=0, vmax=100)
    axs[0, 0].set_title('PCT_CROP Scenario LU file')
    fig.colorbar(im1, ax=axs[0, 0])

    # Plot pct_crop from LU file on top right subplot
    im2 = axs[0, 1].pcolormesh(lon2, lat2, pct_crop2[t,:,:], cmap='YlGn', vmin=0, vmax=100)
    #ax2.set_title('PCT_CROP LU file, time='+ str(t))
    axs[0, 1].set_title('PCT_CROP Historical LU file')
    fig.colorbar(im2, ax=axs[0, 1])

    # Plot difference on lower left subplot
    im3 = axs[1, 0].pcolormesh(lon1, lat1, np.where(area>0, pct_crop1[t,:,:]-pct_crop2[t,:,:], np.nan), cmap='coolwarm', vmin=-10, vmax=10)
    axs[1, 0].set_title('Difference (Scenario-Hist)')
    fig.colorbar(im3, ax=axs[1, 0])

    #Plot time series of area-weighted pct_crop on bottom right subplot
    area_broadcast1 = np.broadcast_to(area, pct_crop1.shape)
    area_broadcast2 = np.broadcast_to(area, pct_crop2.shape)

    pct_crop1_wt = (pct_crop1 * area_broadcast1)/100
    pct_crop2_wt = (pct_crop2 * area_broadcast2)/100
    noluc_crop=np.sum(pct_crop1_wt, axis=(1,2))
    hist=np.sum(pct_crop2_wt, axis=(1,2))
    noluc_crop[165:]= hist[165]
    
    axs[1, 1].plot(np.arange(1850, 2101),np.sum(pct_crop1_wt, axis=(1,2)), label='agtonat, agtoaff')
    axs[1, 1].plot(np.arange(1850, 2101),noluc_crop, label='noluc, nattoaff, agtobio')
    axs[1, 1].plot(np.arange(1850, 2016),np.sum(pct_crop2_wt, axis=(1,2)), label='Historical')
    axs[1, 1].set_title('Crop area (km2)')
    axs[1, 1].legend()

    # Adjust subplots and save figure
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(filename)

    return fig

    
    

def plot_forest(ds1,t, figname_in):
    filename='Figures/' + figname_in + '_' + str(1850+t) +  '.png'
    
    # CLM LU data    
    pct_crop1 = ds1['PCT_CROP'][:]    
    lat1 = ds1['LATIXY'][:]
    lon1 = ds1['LONGXY'][:]
    area = ds1['AREA'][:]
    natpft = ds1['PCT_NAT_PFT'][:, :, :, :]
    pct_forest = np.sum(natpft[:,1:9,:,:], axis=1)
    pct_nonforest = np.sum(natpft[:,9:15,:,:], axis=1) + natpft[:,0,:,:]

    # Create figure
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12), subplot_kw={'projection': 'rectilinear'})
    fig.suptitle('Land Use Data, year' + str(1850+t))

    im1 = axs[0, 0].pcolormesh(lon1, lat1, pct_forest[t,:,:,:], cmap='YlGn', vmin=-100, vmax=200)
    axs[0, 0].set_title('Forest in LU file')
    fig.colorbar(im1, ax=axs[0, 0])

    im2 = axs[0, 1].pcolormesh(lon1, lat1, pct_nonforest[t,:,:,:], cmap='YlGn', vmin=-100, vmax=200)
    #ax2.set_title('PCT_CROP LU file, time='+ str(t))
    axs[0, 1].set_title('Nonforest in LU file')
    fig.colorbar(im2, ax=axs[0, 1])

    # Plot difference on lower left subplot
    im3 = axs[1, 0].pcolormesh(lon1, lat1, pct_forest[t,:,:,:]+pct_nonforest[t,:,:,:], cmap='YlGn', vmin=90, vmax=110)
    axs[1, 0].set_title('Forest + Nonforest in LU file')
    fig.colorbar(im3, ax=axs[1, 0])

    #Plot time series of area-weighted pct_crop on bottom right subplot
    area_broadcast1 = np.broadcast_to(area, pct_crop1.shape)
    area_broadcast2 = np.broadcast_to(area, pct_forest.shape)
    pct_crop1_wt = (pct_crop1 * area_broadcast1)
    pct_forest_wt = (pct_forest * area_broadcast2)
    pct_nonforest_wt = (pct_nonforest * area_broadcast2)
    print(pct_forest_wt.shape)
    axs[1, 1].plot(np.arange(1850, 2101),np.sum(pct_forest_wt, axis=(1,2)), label='Forest')
    #axs[1, 1].plot(np.arange(1850, 2101),np.sum(pct_nonforest_wt, axis=(1,2)), label='NonForest')
    axs[1, 1].plot(np.arange(1850, 2101),np.sum(pct_crop1_wt, axis=(1,2)), label='Crop')
    axs[1, 1].set_title('Area-weighted PCT_CROP time series')
    axs[1, 1].legend()

    # Adjust subplots and save figure
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(filename)

    return fig

    
    
