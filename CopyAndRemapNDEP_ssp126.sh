#!/bin/bash

# Load CDO
module load CDO/1.9.8-intel-2019b NCO/4.9.3-intel-2019b

# Define common file path parts
input_dir=/cluster/shared/noresm/inputdata/
output_dir=${USERWORK}/isimip_forc/Ohter_modified_files/
ndep_file=lnd/clm2/ndepdata/fndep_clm_f09_g17.CMIP6-SSP1-2.6-WACCM_1849-2101_monthly_c191007.nc
isimip_dir=/cluster/shared/noresm/isimip_data/ndep/

# Copy CLM ndep file
cp $input_dir/$ndep_file $output_dir/fndep_clm_f09_g17.CMIP6-SSP1-2.6-WACCM_1849-2101_monthly_ESM2025.nc

# Merge isimip files
if [ -e $output_dir/ndep_isimip_ssp126_0.9x1.25_2015_2100_days.nc ]; then
    echo 'Remaped isimip file exists'
else
    echo 'Remaped isimip file does not exists'
    ncrcat $isimip_dir/ndep-nhx_ssp126* -O $output_dir/ndep_isimip_ssp126_2015_2100.nc 
    ncrcat $isimip_dir/ndep-noy_ssp126* -A $output_dir/ndep_isimip_ssp126_2015_2100.nc 

    # Remap isimip file and change reference time from monthly to daily 
    cdo remapcon2,gridfile1deg.txt  $output_dir/ndep_isimip_ssp126_2015_2100.nc  $output_dir/ndep_isimip_ssp126_0.9x1.25_2015_2100.nc
    cdo setreftime,1850-01-01,00:00:00,1day $output_dir/ndep_isimip_ssp126_0.9x1.25_2015_2100.nc $output_dir/ndep_isimip_ssp126_0.9x1.25_2015_2100_days.nc  
fi