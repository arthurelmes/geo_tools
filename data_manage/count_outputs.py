from glob import glob
import os

# Set relevant dirs
wk_dir = '/media/sf_LinuxShare/outputsTest'

# Set year, band list, product list
year = '2000'
band_list = [1, 2, 3, 4, 5, 6, 7]
prod_list = ['bsa', 'geo', 'iso', 'nbar', 'qa', 'vol', 'wsa']


# Set up complete dictionary of products
hdf_list = []
for prod in prod_list:
    for band in band_list:
        for i in range(1, 367):
            if i < 10:
                doy = '00' + str(i)
            elif i < 100:
                doy = '0' + str(i)
            else:
                doy = str(i)
            hdf_list.append( 'MCD43GF_' + prod + '_Band' + str(band) + \
                                                                  '_' + doy + '_' + year + '_V006.hdf')

# Loop through each *.hdf file and make sure each band/product/year has every DOY accounted for, if not
# spit it out in an errors file. This uses the ideal dictionary created above
for hdf in os.listdir(wk_dir):
    if os.path.isfile(os.path.join(wk_dir, hdf)):
        if hdf in hdf_list:
            hdf_list.remove(hdf)

# Add missing images to err_file
err_file = open('missing_images.txt', 'w')
err_file.close()
err_file = open('missing_images.txt', 'a')
for missing in hdf_list:
    print(missing)
    err_file.write(missing)
    err_file.write('\n')
err_file.close()
