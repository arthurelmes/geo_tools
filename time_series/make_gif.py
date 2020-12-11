import imageio
import os, sys

comparos = ['MCD_VNP', 'MCD_VJ1', 'VJ1_VNP']
tiles = ['h08v05', 'h09v04', 'h11v04', 'h11v09', 'h12v04', 'h16v02', 'h26v04', 'h30v11']

for comparo in comparos:
    for tile in tiles:
        png_dir = '/data/mcd_vj1_vnp_comparo/' + comparo + '/' + tile + '/'
        gif_dir = '/home/arthur/Dropbox/projects/modis_viirs_continuity/sensor_intercompare/'

        gif_list = [file for file in os.listdir(png_dir) if file.endswith('.png')]
        gif_list.sort()

        images = []

        for file_name in gif_list: images.append(imageio.imread(png_dir + file_name))

        imageio.mimsave(gif_dir + comparo + '_' + tile + '.gif', images, 'GIF', duration=0.1)
