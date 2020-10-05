#!/bin/bash

## WARNING: Currently only works with manual tile bounding coords (in meters from origin, I think?), which must be passed in manually. Get by looking at extent in QGIS or similar.
## TODO convert bounding coordinates from ll to meters so this is automated. Shortcut/hurry mode, just write them down in file for all tiles.

## h10v04 UL: -8895604.1573329996317625 5559752.5983330002054572 LR: -7783653.6376670002937317 4447802.0786669999361038
## h11v04 UL: -7783653.6376670002937317 5559752.5983330002054572 LR: -6671703.1179999997839332 4447802.0786669999361038
## h11v09 UL: -7783653.6376670002937317 0.0000000000000000 LR:-6671703.1179999997839332 -1111950.5196670000441372  
## h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
## h13v04 UL: -5559752.5983330002054572 5559752.5983330002054572 LR: -4447802.0786669999361038 4447802.0786669999361038
## h15v02 UL: -3335851.5589999998919666 7783653.6376670002937317 LR: -2223901.0393329998478293 6671703.1179999997839332
## h16v00 UL: -2223901.0393329998478293 10007554.6769999992102385 LR: -1111950.5196670000441372 8895604.1573329996317625 
## h16v01 UL: -2223901.0393329998478293 8895604.1573329996317625 LR: -1111950.5196670000441372 7783653.6376670002937317
## h16v02 UL: -2223901.0393329998478293 7783653.6376670002937317 LR: -1111950.5196670000441372 6671703.1179999997839332
## h30v11 UL: 13343406.2359999995678663 -2223901.0393329998478293 LR: 14455356.7556669991463423 -3335851.5589999998919666

in_dir=$1 
out_dir=$2

srs_str="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/qa/ ]; then
    mkdir ${out_dir}/qa/
fi

if [ ! -d ${out_dir}/nbar/ ]; then
    mkdir ${out_dir}/nbar/
fi

for h5 in $in_dir/*.h5
do
    case $h5 in
	*h15v02*)
	    echo "Tile h15v02 detected."
	    ul_coord='-3335851.5589999998919666 7783653.6376670002937317'
	    lr_coord='-2223901.0393329998478293 6671703.1179999997839332'
	    ;;
	*h16v00*)
	    echo "Tile h16v00 detected."
	    ul_coord='-2223901.0393329998478293 10007554.6769999992102385'
	    lr_coord='-1111950.5196670000441372 8895604.1573329996317625'
	    ;;
	*h16v01*)
	    echo "Tile h16v01 detected."
	    ul_coord='-2223901.0393329998478293 8895604.1573329996317625'
	    lr_coord='-1111950.5196670000441372 7783653.6376670002937317'
	    ;;
	*h16v02*)
	    echo "Tile h16v02 detected."
	    ul_coord='-2223901.0393329998478293 7783653.6376670002937317'
	    lr_coord='-1111950.5196670000441372 6671703.1179999997839332'
	    ;;
	*h12v04*)
	    echo "Tile h12v04 detected."
	    ul_coord='-6671703.1179999997839332 5559752.5983330002054572'
	    lr_coord='-5559752.5983330002054572 4447802.0786669999361038'
	    ;;
	*h11v09*)
	    echo "Tile h11v09 detected."
	    ul_coord='-7783653.6376670002937317 0.0000000000000000'
	    lr_coord='-6671703.1179999997839332 -1111950.5196670000441372'
	    ;;
	*h30v11*)
	    echo "Tile h30v11 detected."
	    ul_coord='13343406.2359999995678663 -2223901.0393329998478293'
	    lr_coord='14455356.7556669991463423 -3335851.5589999998919666'
	    ;;
	*)
	    echo "Tile not found! Please open script and define bounding coords."
	    ul_coord=''
	    lr_coord=''
	    ;;
    esac

    filename=$(basename -- $h5)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"

    # for nbar
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M1 ${out_dir}/nbar/${filename}_nbar_b1.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M10 ${out_dir}/nbar/${filename}_nbar_b10.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M11 ${out_dir}/nbar/${filename}_nbar_b11.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M2 ${out_dir}/nbar/${filename}_nbar_b2.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M3 ${out_dir}/nbar/${filename}_nbar_b3.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M4 ${out_dir}/nbar/${filename}_nbar_b4.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M5 ${out_dir}/nbar/${filename}_nbar_b5.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M7 ${out_dir}/nbar/${filename}_nbar_b7.tif
    gdal_translate -a_nodata 32767 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Nadir_Reflectance_M8 ${out_dir}/nbar/${filename}_nbar_b8.tif

    # for qa
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M1 ${out_dir}/qa/${filename}_qa_b1.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M10 ${out_dir}/qa/${filename}_qa_b10.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M11 ${out_dir}/qa/${filename}_qa_b11.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M2 ${out_dir}/qa/${filename}_qa_b2.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M3 ${out_dir}/qa/${filename}_qa_b3.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M4 ${out_dir}/qa/${filename}_qa_b4.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M5 ${out_dir}/qa/${filename}_qa_b5.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M7 ${out_dir}/qa/${filename}_qa_b7.tif
    gdal_translate -a_nodata 255 -a_srs "${srs_str}" -a_ullr $ul_coord $lr_coord -of GTiff HDF5:"${in_dir}/${filename}"://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_M8 ${out_dir}/qa/${filename}_qa_b8.tif

done


