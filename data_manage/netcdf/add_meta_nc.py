#!/home/arthur.elmes/software/anaconda3/envs/geo_nc/bin/python

from netCDF4 import Dataset
import datetime
import os
import numpy as np

now = datetime.datetime.now()
wkdir = "/penobscot/data01/arthur.elmes/MCD12Q1_merged/subgrid/"

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

    # Print global attributes to check
    for name in rootgrp.ncattrs():
        print("Global attr {} = {}".format(name, getattr(rootgrp, name)))
    rootgrp.close()
for (root, dirs, files) in os.walk(wkdir):
    for fl in files:
        fl_name = root + os.sep + fl
        if fl_name.endswith(".nc"):
            print("Adding attributes to: " + fl_name)
            set_global_atts(fl_name)
