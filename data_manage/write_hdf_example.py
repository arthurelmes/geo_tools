### Example from docs http://hdfeos.github.io/pyhdf/modules/SD.html#writing
# Import SD and numpy. 
from pyhdf.SD import *
from numpy import *

fileName = 'template.hdf' 
# Create HDF file. 
hdfFile = SD(fileName, SDC.WRITE|SDC.CREATE)

# Assign a few attributes at the file level 
hdfFile.author = 'It is me...'
hdfFile.priority = 2

# Create a dataset named 'd1' to hold a 3x3 float array. 
d1 = hdfFile.create('d1', SDC.FLOAT32, (3,3)) 

# Set some attributs on 'd1' 
d1.description = 'Sample 3x3 float array' d1.units = 'celsius' 
# Name 'd1' dimensions and assign them attributes. 
dim1 = d1.dim(0)
dim2 = d1.dim(1)
dim1.setname('width')
dim2.setname('height')
dim1.units = 'm'
dim2.units = 'cm'

# Assign values to 'd1'
d1[0] = (14.5, 12.8, 13.0) # row 1
d1[1:] = ((-1.3, 0.5, 4.8), # row 2 and
          (3.1, 0.0, 13.8)) # row 3

# Close dataset 
d1.endaccess() 

# Close file 
hdfFile.end()
