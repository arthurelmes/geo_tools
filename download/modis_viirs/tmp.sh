#!/bin/bash

for year in {2000..2020};
do
    ./download_viirs_modis_laadsweb.sh MCD43D40 6 ${year} 32 60  "h00v00" /ipswich/data02/arthur.elmes/
    ./download_viirs_modis_laadsweb.sh MCD43D31 6 ${year} 32 60  "h00v00" /ipswich/data02/arthur.elmes/

done

