#!/bin/bash

img_dir="/home/arthur/Dropbox/projects/climo_mcd43d61/MCD43D61/tif/"
out_dir="/home/arthur/Dropbox/projects/climo_mcd43d61/MCD43D61/tif/out_directoryly"
#template_img="/ipswich/data01/arthur.elmes/bsky/tif/qa_screened_merged/greenland_entire_island_zeros.tif"

tmp_dir=${out_dir}/tmp/
if [ ! -d "${tmp_dir}" ];
then
    mkdir -p ${tmp_dir}
fi

img_list=(`find ${img_dir} -maxdepth 1 -type f -name "*.tif"`)

# create the temporary processing files that will be added to get average
# this is necessary because otherwise NoData turns the whole pixel stack into null

if [ ! -z "${img_list}" ];
then    
    for tif in ${img_list[@]};
    do
    	echo "Finding valid pixels to average for: ${tif}"
    	gdal_translate -q -of VRT ${tif} ${tif}_nodata_is_zero.vrt -a_nodata 0
    	gdal_calc.py --quiet --overwrite -A ${tif}_nodata_is_zero.vrt --outfile=${tif}_valid_pix.tif \
    		     --calc="1*(A<=1000)+0*(A==32767)"
    	gdal_calc.py --quiet --overwrite -A ${tif}_nodata_is_zero.vrt --outfile=${tif}_to_add.tif \
    		     --calc="A*(A<=1000.0)+0*(A==32767)" --NoDataValue=-999

    	mv ${img_dir}*_to_add.tif ${tmp_dir}
    	mv ${img_dir}*_valid_pix.tif ${tmp_dir}
    	rm ${img_dir}*.vrt
    done

fi

img_list_num=(`find ${tmp_dir} -maxdepth 1 -type f -name "*.tif*_to_add.tif"`)
img_list_den=(`find ${tmp_dir} -maxdepth 1 -type f -name "*.tif*_valid_pix.tif"`)
echo "Image list for numerator: ${img_list_num}"
echo "Image list for demonimator ${img_list_den}"

if [ ! -z "${img_list_num}" ];
then
    
    # create a new blank raster to start accumulating into -- copy
    # the first raster and multiply the whole thing by 0 to start fresh
    cp ${img_list_num[0]} ${tmp_dir}/numerator.tif
    cp ${img_list_den[0]} ${tmp_dir}/denominator.tif

    echo "Creating blank numerator and denominator rasters to start with."
    gdal_calc.py --quiet --overwrite -A ${tmp_dir}/numerator.tif \
		 --outfile=${tmp_dir}/numerator.tif --calc="A*0"

    gdal_calc.py --quiet --overwrite -A ${tmp_dir}/denominator.tif \
		 --outfile=${tmp_dir}/denominator.tif --calc="A*0"

    
    imga_num=${tmp_dir}/numerator.tif
    imga_den=${tmp_dir}/denominator.tif
    img_avg=${tmp_dir}/average.tif
    
    # now add all the numerators together
    # and all the denominators together
    len=`echo ${#img_list_num[@]}`
    for img in $(seq 0 "$((len-1))");
    do
    	# now add each new image to the initial raster to get the acumulation
    	imgb_num=`echo ${img_list_num[$img]}`
	imgb_den=`echo ${img_list_den[$img]}`
	
    	#calc_str="A + B"
    	gdal_cmd1_num=`echo gdal_calc.py -A ${imga_num} -B ${imgb_num} --outfile ${imga_num} --overwrite --quiet --calc=\"A+B\"`
    	gdal_cmd1_den=`echo gdal_calc.py -A ${imga_den} -B ${imgb_den} --outfile ${imga_den} --overwrite --quiet --calc=\"A+B\"`

	#echo $gdal_cmd1
	echo "Calculating numerator and denominator rasters"
    	eval $gdal_cmd1_num
	eval $gdal_cmd1_den
    done

    # then divide by the numerator by the denominator for that day to get the mean
    gdal_cmd2=`echo gdal_calc.py -A ${imga_num} -B ${imga_den} --outfile ${img_avg} --overwrite --quiet --type=Float32 --calc=\"A/B\"`
    echo "Calculating average per pixel: ${gdal_cmd2}"
    eval $gdal_cmd2
    rm ${tmp_dir}/*tif_to_add.tif
    rm ${tmp_dir}/*tif_valid_pix.tif
    mv ${tmp_dir}/*average*.tif ${out_dir}		
fi
