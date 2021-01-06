import pandas as pd
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import os, sys


f1 = sys.argv[1]
f2 = sys.argv[2]
f1_qa = sys.argv[3]
f2_qa = sys.argv[4]

f1_name = os.path.basename(f1)
f2_name = os.path.basename(f2)
out_file_name = f1_name + "_vs_" + f2_name

with rio.open(f1) as b1:
    b1_data = b1.read(1)

with rio.open(f2) as b2:
    b2_data = b2.read(1)

with rio.open(f1_qa) as b1_qa:
    b1_data_qa = b1_qa.read(1)

with rio.open(f2_qa) as b2_qa:
    b2_data_qa = b2_qa.read(1)

# qa screen
b1_data = b1_data.flatten()
b2_data = b2_data.flatten()
b1_data_qa = b1_data_qa.flatten()
b2_data_qa = b2_data_qa.flatten()
df = pd.DataFrame({'b1':b1_data, 'b2':b2_data, 'b1_qa':b1_data_qa, 'b2_qa':b2_data_qa})

mask_b1 = df[ df['b1_qa'] > 0].index
df.drop(mask_b1, inplace=True)

mask_b2 = df[ df['b2_qa'] > 0].index
df.drop(mask_b2, inplace=True)

df['b1'] = df['b1'] * 0.001
df['b2'] = df['b2'] * 0.001

# plot

fig, ax = plt.subplots(figsize=(15,10))
fig.patch.set_facecolor('black')

#plt.figure(figsize=(10,10))

hist = plt.hist2d(df['b1'], df['b2'], bins=200,
                  norm=LogNorm(), range=[[0, 1.0], [0, 1.0]], cmap=plt.cm.YlGn)
ax.set_facecolor('black')
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')

#fig = plt.colorbar(hist[3])
ax.set_ylim(0.0, 1.0)
ax.set_xlim(0.0, 1.0)
ax.set_xlabel(f1_name)
ax.set_ylabel(f2_name)
ax.set_title('')

# 1:1 line
lims = [
    np.min([plt.xlim(), plt.ylim()]),  # min of both axes
    np.max([plt.xlim(), plt.ylim()]),  # max of both axes
]
plt.plot(lims, lims, 'deeppink', alpha=0.75, zorder=1)
plt.xlim(lims)
plt.ylim(lims)

print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=out_file_name))
fig.savefig('{out_dir}/{plt_name}.png'.format(out_dir=sys.argv[5], plt_name=out_file_name), facecolor='black')