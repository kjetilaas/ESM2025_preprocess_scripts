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

