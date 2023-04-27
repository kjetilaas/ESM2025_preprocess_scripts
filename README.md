# ESM2025 preprocessing scripts
Repo with scripts to modify CLM input files to match ISIMIP input files for ESM2025 simulations. 

### CO2 (Modify_CO2.py)
- overwrite co2 timeseries

### Surface and Land Use data (Modify_landuse.py)
- Remap original (0.5 deg) isimip LU file to 1.9x2.5 grid (defined in gridfile.txt)
- Replace PCT_CROP in surface and landuse files, using original pct_natveg + pct_crop as upper limit
    - this keeps the original CLM cft distribution within each grid cell, and only modifies the crop fraction
    - it also ignores some small crop fractions in grid cells with 100 % lake in original CLM file.
- Scale PCT_NATVEG to match new crop area

### Atmospheric forcing (separate repo, ctsm_isimip_prepost)
- Calculates diurnal (3-hourly) cycle for each day of year based on 1970-2014 GSWP3 data. 
- Adds diurnal cycle to daily bias-corrected ESM output from ISIMIP, excluding precipitation data which use dainly mean values. 

### Lightning (not modified)
- Use default CLM file. 
    - Both ISIMIP and default CLM input files are based on Cecil, Daniel J. 2006 LIS/OTD 0.5 Degree High Resolution Monthly Climatology (HRMC). However, ISIMIP includes only monthly data, while CLM include diurnal (2-hourly) cycle from LIS/OTD 2.5 Degree Low Res Annual Diurnal Climatology (LRADC), processes by Fang Li and Erik Kluzek. 

### Population data (not modified)
- ISIMIP use HYDE v3.3 (Klein Goldewijk et al., 2022, in preparation)
- CLM use "Klein Goldewijk, K., A. Beusen, J.Doelman and E. Stehfest, New Holocene land use estimates; HYDE 3.2 (2017), ESSD"
- HYDE v3.2 and 3.3 appears relatively similar. As these data are only used in the fire module, we choose not to modify these.

### GDP data (not modified)
- Both are based on Wold Development Indicator database. Used only in the fire model of CLM, and therefore not modified. 

### N-deposition (Modify_ndep.py)
- Remap isimip to 0.9x1.25 clm input grid.
- Overwrite monthly ndep data in clm input file
- Set other ndep values to -9999 (to make sure they are not used)