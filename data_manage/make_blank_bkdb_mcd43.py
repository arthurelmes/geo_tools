""" This script takes in a 'template' hdf from the MCD43 backup database and makes it into a completely
blank version of itself, with fill values for all SDSs.
Author: Arthur Elmes
2020-06-16
Much of the structure of this code comes from two sources:
https://www.science-emergence.com/Articles/How-to-read-a-MODIS-HDF-file-using-python-/
http://hdfeos.github.io/pyhdf/modules/SD.html#writing
"""

from pyhdf.SD import SD, SDC
import os
import numpy as np
import pprint

fname = 'BRDF_DB.A2001001.h12v04.002.2005235120000.hdf'
workspace = '/home/arthur/Dropbox/projects/mcd43_nrt/'
os.chdir(workspace)

# 'BRDF_Model_ID', 'BRDF_Albedo_Quality',
sds_list = ['BRDF_Albedo_Parameters_S1', 'BRDF_Albedo_Parameters_S2', 'BRDF_Albedo_Parameters_S3']

#

hdf_ds = SD(fname, SDC.WRITE)
datasets_dict = hdf_ds.datasets()

# print sds names
for idx, sds in enumerate(datasets_dict.keys()):
    print(idx, sds)

# select each parameter sds, make a np array full of fill values
for sds in sds_list:
    dataset_param = hdf_ds.select(sds)
    #pprint.pprint(dataset_param.attributes())
    data_np = dataset_param[:, :]
    fill_arr_param = np.full(data_np.shape, 32767, dtype='int16')
    dataset_param[:, :] = fill_arr_param
    dataset_param.endaccess()

# do the same as above for the model id sds, make a np array full of fill values
dataset_mdl_id = hdf_ds.select('BRDF_Model_ID')
data_np_mdl_id = dataset_mdl_id[:, :]
fill_arr_mdl_id = np.full(data_np_mdl_id.shape, 255, dtype='uint8')
dataset_mdl_id[:, :] = fill_arr_mdl_id
#pprint.pprint(dataset_mdl_id.attributes())
dataset_mdl_id.endaccess()

# do the same as above for the qa sds, make a np array full of fill values
dataset_qa = hdf_ds.select('BRDF_Albedo_Quality')
data_np_qa = dataset_qa[:, :]
fill_arr_qa = np.full(data_np_qa.shape, 65535, dtype='uint16')
dataset_qa[:, :] = fill_arr_qa
#pprint.pprint(dataset_qa.attributes())
dataset_qa.endaccess()

hdf_ds.end()
