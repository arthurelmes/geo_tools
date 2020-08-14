#!/bin/bash

dl_dir=/muddy/data05/arthur.elmes/lance
# Download selected tiles of Lance-processed MOD09GA and MYD09GA NRT products

# MxD09

# New England
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h12v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h12v04/

# Sahel
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h17v07/

# SW USA
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h09v05/

# N Chile
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h11v11/

# N Amazon
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h11v08/

# NW China
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MOD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MOD09GA/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MYD09GA/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MYD09GA/h24v04/




# Download selected tiles of Lance-processed MCD43 products

# New England
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h12v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h12v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h12v04/ 
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h12v04/ 

# Sahel
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h17v07/

# SW USA
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h09v05/

# N Chile
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h11v11/

# N Amazon
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h11v08/

# NW China
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A1/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A2/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A3/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.hdf "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/6/MCD43A4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/MCD43A4/h24v04/


# VNP09

# New England
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h12v04/

# Sahel
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h17v07/

# SW USA
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h09v05/

# N Chile
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h11v11/

# N Amazon
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h11v08/

# NW China
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP09GA_NRT/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP09GA/h24v04/



# Download selected tiles of Lance-processed VNP43 products

# New England
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h12v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h12v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h12v04/ 
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h12v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h12v04/ 

# Sahel
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h17v07/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h17v07*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h17v07/

# SW USA
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h09v05/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h09v05*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h09v05/

# N Chile
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h11v11/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v11*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h11v11/

# N Amazon
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h11v08/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h11v08*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h11v08/

# NW China
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA1N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA1/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA2N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA2/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA3N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA3/h24v04/
wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=4 -A *h24v04*.h5 "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5000/VNP43MA4N/Recent" --header "Authorization: Bearer A5041508-D88A-11E8-858A-7C099B439298" -P $dl_dir/VNP43MA4/h24v04/
