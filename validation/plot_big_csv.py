import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os, sys
from csv import reader
from glob import glob


def make_ax(x, y, ax):
    # This is a density scatterplot; maybe tweak bins to get the look right
    hist = ax.hist2d(x, y, bins=200, norm=LogNorm(), range=[[0, 1.0], [0, 1.0]], cmap=plt.cm.YlGn)

    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_xlabel(sample.columns[0])
    ax.set_ylabel(sample.columns[1])
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_title(tile)
    ax.title.set_color('white')

    # Add x=y line
    lims = [
        np.min([plt.xlim(), plt.ylim()]),  # min of both axes
        np.max([plt.xlim(), plt.ylim()]),  # max of both axes
    ]

    # Plot limits against each other for 1:1 line
    ax.plot(lims, lims, 'y-', alpha=0.75, zorder=1)
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    # Calculate RMSE and Mean Bias, always tile 1 minus tile 2, i.e. x - y
    rmse = np.nanmean((x - y) ** 2) ** 0.5
    mb = np.nanmean(x) - np.nanmean(y)

    # Add text box with RMSE and mean bias
    textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.4f$' % (rmse, ),
        r'$\mathrm{MeanBias}=%.4f$' % (mb, )))

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.95, textstr, fontsize=10, verticalalignment='top', bbox=props)
    # print('Made plot for {x} vs {y}'.format(x=sample.columns[0], y=sample.columns[1]))
    return hist


# Here, loop over all pairs of x,y from the different tiles, which are in
# different CSV files
tiles = ['h08v05', 'h09v04', 'h11v04', 'h12v04', 'h26v04', 'h30v11']

workspace = '/ipswich/data02/arthur.elmes/comparo_results/csv/'

# TODO define the number of rows based on length of csv_names
fig, ax = plt.subplots(len(tiles), 3, figsize=(7, 3))
fig.tight_layout(pad=3)

for tile in tiles:
    csv_names = glob(os.path.join(workspace, tile) + '/*all.csv')
    # Maybe experiment with this?
    chunksize = 10 ** 6

    # Set up the figure first, then fill with axes

    # ax counter
    i = 0
    year = ''
    tile = ''
    for csv_name in csv_names:
        print(csv_name)
        # Get the header names
        header = []
        try:
            with open(csv_name, 'r') as read_object:
                csv_reader = reader(read_object)
                header = next(csv_reader)

            # Pull the tile and year from filename
            tile = os.path.basename(csv_name)[:6]
            year = os.path.basename(csv_name)[7:11]

            # Create an empty df to add to
            sample = pd.DataFrame(columns=header)

            # The csvs are so huge we have to step through them in chunks
            for chunk in pd.read_csv(csv_name, chunksize=chunksize):
                subset = chunk.loc[np.random.choice(chunk.index, 30, replace=False)]
                sample = sample.append(subset)

            # Mask out 32.767 values which should have already been removed!!
            nodata_masked = np.ma.masked_array(sample, sample == 32.767)
            sample_masked = np.ma.filled(nodata_masked, np.nan)

            # Set the x and y from the masked data
            x = sample_masked[:, 0]
            y = sample_masked[:, 1]

            make_ax(x, y, ax[i])
            i += 1
        except:
            print("File could not be opened!")
            
fname = os.path.join(workspace, tile) + '/' + tile + '_2019_scatterplots.png'
fig.savefig(fname)
