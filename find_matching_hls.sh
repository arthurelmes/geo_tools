#!/bin/bash

L2A_dir=/lovells/data02/arthur.elmes/S2/HLS_comparison/05WPM/L2A/
HLS_dir=/lovells/data01/arthur.elmes/HLS/sample_hls/S30/2020/05/W/P/M/

hdf_to_jp2 () {
    in_file_hls=$1
    template_file_s2=$2
    band=$3

    template_file_s2_base=$(basename -- $template_file_s2)
    IFS="_"
    read -ra band_part_1 <<< "$template_file_s2_base"
    band=${band_part_1[2]}
    IFS=" "
    gdal_translate -of JP2OpenJPEG HDF4_EOS:EOS_GRID:'"'${in_file_hls}'"':Grid:${band} ${template_file_s2}
}

for safe in ${L2A_dir}/* ;
do
    for jp2 in ${safe}/GRANULE/*/IMG_DATA/R20m/* ;
    do
	#echo $jp2
	case $jp2 in
	    *"B02"*|*"B03"*|*"B04"*|*"B11"*|*"B12"*|*"B8A"*|*"SCL"*)
		#echo "convert!"
		jp2_file_base=$(basename -- $jp2)
		IFS="_"
		read -ra file_parts <<< "$jp2_file_base"
		datepart=${file_parts[1]}
		img_date=`date +"%Y%j" --date="${datepart::8}"`
		tile=${file_parts[0]}
		band=${file_parts[2]}
		IFS=" "  

		echo $band
		
		hls_match=`find ${HLS_dir} -type f -name "HLS.S30.${tile}.${img_date}*.hdf"`
		echo "Converting bands from: $hls_match into: $jp2"
		hdf_to_jp2 "${hls_match}" "${jp2}" "${band}"
		;;
	    *)
		echo "Don't convert this band."
		;;
	esac
	
    done
    
done
