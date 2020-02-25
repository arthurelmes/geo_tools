#!/home/arthur.elmes/software/anaconda3/envs/geo_nc/bin/python

from netCDF4 import Dataset
import datetime
import os
import sys
import numpy as np

def calc_lat(nc):
    # the modis grid uses upper left corner as lat/long orign, and stores latitude positive to 
    # negative in the lat array. Nancy (and modelers generally?) need the lat/lon to represtn
    # cell centers instead of corners, and for latitude to be stored "bottum up", i.e. with
    # negative/southern latitudes at the beginning of the lat array.
    with Dataset(nc, "r+") as rootgrp:
        lat = rootgrp.variables['lat'][:]
        new_lat = np.zeros(lat.shape)
        lon = rootgrp.variables['lon'][:]
        new_lon = np.zeros(lon.shape)

        # iterate over blank lat array and fill in calculated values that flip and translate the values
        i = 1
        for y in np.nditer(new_lat):
            # calculate new value of latitude based on index and spatial resolution of 30 arcseconds
            # note geographic projection, so map units are degrees, 1/120 is 30 arcseconds
            #y = 90 - (i * (1/240))
            y = -90 + (1/120)*(0.5 + i - 1 )
            new_lat[i - 1] = y
            i += 1

        # iterate over blank lon array and fill in calculate values that translate the values
        j = 1
        for x in np.nditer(new_lon):
            x = -180 + (1/120)*(0.5 + j - 1)
            new_lon[j - 1] = x
            j += 1
        rootgrp['lat'][:] = new_lat
        rootgrp['lon'][:] = new_lon
        check_lat = rootgrp['lat'][:]
        check_lon = rootgrp['lon'][:]
    #rootgrp.close()
    
def set_global_atts(nc):
    # netcdf global attributes are set by modifying the root group's attributes.
    # The root group is analogous to unix root dir, and contains all vars (similar to SDS in hdf)
    with Dataset(nc, "r+") as rootgrp:

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
    #rootgrp.close()

def main(wkdir):
    for (root, dirs, files) in os.walk(wkdir):
        for fl in files:
            fl_name = root + os.sep + fl
            if fl_name.endswith(".nc"):
                print("Calculating latitude shift for: " + fl_name)
                calc_lat(fl_name)
                set_global_atts(fl_name)

if __name__ == '__main__':
    now = datetime.datetime.now()
    main(sys.argv[1])
