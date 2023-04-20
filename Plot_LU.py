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