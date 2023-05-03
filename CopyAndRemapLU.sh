#!/bin/bash

# Load CDO
module load CDO/1.9.8-intel-2019b

# Define common file path parts
input_dir=/cluster/shared/noresm/inputdata/
output_dir=${USERWORK}/isimip_forc/Ohter_modified_files/
lu_file=lnd/clm2/surfdata_map/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_c170824.nc
surf_file=lnd/clm2/surfdata_map/release-clm5.0.18/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_c190304.nc
landuse_file=../From_Spirit/landuse/landuse-totals_histsoc_annual_1850_2014.nc

# Copy LU file
cp $input_dir/$lu_file $output_dir/landuse.timeseries_1.9x2.5_hist_78pfts_CMIP6_simyr1850-2015_ESM2025.nc

# Copy surface file
cp $input_dir/$surf_file $output_dir/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_ESM2025.nc

# Remap isimip landuse file to 1.9x2.5 (intermediate file)
cdo remapcon2,gridfile.txt $landuse_file $output_dir/landuse-totals_histsoc_1.9x2.5deg_annual_1850_2014.nc