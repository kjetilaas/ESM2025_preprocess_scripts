import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def plot_surface(ds, figname_in):
    filename='Figures/' + figname_in + '.png'
    # CLM LU data
    pct_crop = ds['PCT_CROP'][:]    
    pct_natveg = ds['PCT_NATVEG'][:]    
    pct_lake = ds['PCT_LAKE'][:]  
    pct_glacier = ds['PCT_GLACIER'][:]  
    pct_urban = ds['PCT_URBAN'][:]  
    sum_urb = np.sum(pct_urban, axis=0)
    lat = ds['LATIXY'][:]
    lon = ds['LONGXY'][:]
    area = ds['AREA'][:]
    
    # Create figure
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12), subplot_kw={'projection': 'rectilinear'})
    fig.suptitle('Surface data')

    # Plot pct_crop on top left subplot
    im1 = axs[0, 0].pcolormesh(lon, lat, pct_crop, cmap='YlGn', vmin=0, vmax=100)
    axs[0, 0].set_title('PCT_CROP surf file')
    fig.colorbar(im1, ax=axs[0, 0])

    # Plot pct_crop from LU file on top right subplot
    im2 = axs[0, 1].pcolormesh(lon, lat, pct_natveg, cmap='YlGn', vmin=0, vmax=100)    
    axs[0, 1].set_title('PCT_NATVEG surf file')
    fig.colorbar(im2, ax=axs[0, 1])

    # Plot difference on lower left subplot
    pct_all=pct_crop+pct_natveg+ pct_lake + pct_glacier + sum_urb

    im3 = axs[1, 0].pcolormesh(lon, lat, pct_all, cmap='YlGn', vmin=90, vmax=110)
    axs[1, 0].set_title('PCT_CROP + PCT_NATCEG + PCT_GLACIER + PCT_LAKE3')
    fig.colorbar(im3, ax=axs[1, 0])

    #Check for values outside range
    maskAbove = pct_all > 100.0000000000001
    maskBelow = pct_all < 0.
    np.set_printoptions(precision=20)
    print('here')
    print(pct_all[maskAbove])
    print(pct_all[maskBelow])

#    pct_all = np.where(pct_all > 100, 200, pct_all)
#    pct_all = np.where(pct_all < 0, -200, pct_all)
    im4 = axs[1, 1].pcolormesh(lon, lat, pct_all, cmap='RdBu_r', vmin=99.9999, vmax=100.0001)    
    axs[1, 1].set_title('Points with tot area > 100% (set to 200)')
    fig.colorbar(im4, ax=axs[1, 1])

    # Adjust subplots and save figure
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(filename)

    return fig