#!/home/arthur.elmes/software/anaconda3/envs/geo_nc/bin/python

from netCDF4 import Dataset
import datetime
import os
import numpy as np

now = datetime.datetime.now()
wkdir = "/penobscot/data01/arthur.elmes/test/"

def set_global_atts(nc):    
    # netcdf global attributes are set by modifying the root group's attributes.
    # The root group is analogous to unix root dir, and contains all vars (similar to SDS in hdf)
    rootgrp = Dataset(nc, "r+")

    # Create/set global attributes
    rootgrp.description = "Partitioning of MODIS MCD12Q1 V006 L3 IGBP and PFT land cover" \
                          "for the Ent Global Vegetation Structure Dataset, in geographic" \
                          "coordinates for a Climate Modeling Grid (CMG)."
    rootgrp.creator="Qingsong Sun, Arthur Elmes, Crystal Schaaf, Nancy Y. Kiang"
    rootgrp.contact="nancy.y.kiang@nasa.gov, qingsong.sun@nasa.gov, arthur.elmes@umb.edu"
    rootgrp.date_created=now.strftime("%Y-%m-%d")

    print(rootgrp.variables.keys())
    lat_var = rootgrp.variables['lat']
    lon_var = rootgrp.variables['lon']
#    print(lat_var.ncattrs())
#    print(lon_var.ncattrs())
    
    print(lat_var.getncattr('units'))
    lat_values = rootgrp.variables['lat'][:]
    print(lat_values)
    
    print(lon_var.getncattr('units'))
    lon_values = rootgrp.variables['lon'][:]
    print(lon_values)

    # Print global attributes to check
    #for name in rootgrp.ncattrs():
    #    print("Global attr {} = {}".format(name, getattr(rootgrp, name)))

    rootgrp.close()

def print_test_data(nc):
    pass
        
for (root, dirs, files) in os.walk(wkdir):
    for fl in files:
        fl_name = root + os.sep + fl
        if fl_name.endswith(".nc"):
            #print("Adding attributes to: " + fl_name)
            set_global_atts(fl_name)
