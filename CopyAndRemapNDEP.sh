#!/bin/bash

# Load CDO
module load CDO/1.9.8-intel-2019b NCO/4.9.3-intel-2019b




# Define common file path parts
input_dir=/cluster/shared/noresm/inputdata/
output_dir=/cluster/work/users/kjetisaa/isimip_forc/Ohter_modified_files/
ndep_file=lnd/clm2/ndepdata/fndep_clm_hist_b.e21.BWHIST.f09_g17.CMIP6-historical-WACCM.ensmean_1849-2015_monthly_0.9x1.25_c180926.nc

isimip_dir=/cluster/shared/noresm/isimip_data/ndep/

# Copy CLM ndep file
cp $input_dir/$ndep_file $output_dir/fndep_clm_hist_b.e21.BWHIST.f09_g17.CMIP6-historical-WACCM.ensmean_1849-2015_monthly_0.9x1.25_ESM2025.nc

# Merge isimip files (hacky, but files are not too big so ok for now)
#ncrcat $isimip_dir/ndep-nhx_* -O $output_dir/temp_nhx_1850_2021.nc
#ncrcat $isimip_dir/ndep-noy_* -O $output_dir/temp_noy_1850_2021.nc
#ncks -A $output_dir/temp_nhx_1850_2021.nc $output_dir/temp_noy_1850_2021.nc 
#ncap2 -s 'NDEP=nhx+noy;' -O $output_dir/temp_noy_1850_2021.nc $output_dir/ndep_isimip_1850_2021.nc 
#rm $output_dir/temp_*

ncrcat $isimip_dir/ndep-nhx_* -O $output_dir/ndep_isimip_1850_2021.nc 
ncrcat $isimip_dir/ndep-noy_* -A $output_dir/ndep_isimip_1850_2021.nc 
#ncap2 -s 'NDEP=nhx+noy;' -O $output_dir/temp_ndep_isimip_1850_2021.nc $output_dir/ndep_isimip_1850_2021.nc 
#rm $output_dir/temp_ndep_isimip_1850_2021.nc 

# Remap isimip landuse file to 1.9x2.5 (intermediate file)
cdo remapcon2,gridfile1deg.txt  $output_dir/ndep_isimip_1850_2021.nc $output_dir/ndep_isimip_0.9x1.25_1850_2021.nc
cdo setreftime,1850-01-01,00:00:00,1day $output_dir/ndep_isimip_0.9x1.25_1850_2021.nc $output_dir/ndep_isimip_0.9x1.25_1850_2021_days.nc  