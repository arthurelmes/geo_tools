import imageio
import os, sys

root_dir = '/ipswich/data02/arthur.elmes/comparo_results/png/'
comparos = ['MCD_VNP', 'MCD_VJ1', 'VJ1_VNP']
tiles = ['h08v05', 'h09v04', 'h11v04', 'h11v09', 'h12v04', 'h16v02', 'h26v04', 'h30v11']
m_bands = ['Band1', 'Band2', 'Band3', 'Band4', 'Band5', 'Band6', 'Band7', 'nir', 'shortwave', 'vis']
v_bands = ['M3', 'M4', 'M5', 'M7', 'M8', 'M10', 'M11', 'nir', 'shortwave', 'vis']
products = ['A3', 'A4']

for product in products:
    for m_band in m_bands:
        for comparo in comparos:
            if "MCD" in comparo:
                for tile in tiles:
                    png_dir = os.path.join(root_dir, tile, comparo, product, m_band + '/')
                    print(png_dir)
                    gif_dir = root_dir
                    gif_list = [file for file in os.listdir(png_dir) if file.endswith('.png')]
                    gif_list.sort()
                    images = []
                    for file_name in gif_list: images.append(imageio.imread(png_dir + file_name))
                    try:
                        imageio.mimsave(gif_dir + comparo + '_' + product +'_' + tile + '_' + m_band + '.gif', images, 'GIF', duration=0.1)
                    except:
                        print('failed to make gif for {} {} {} {}'.format(comparo, product, tile, m_band))

    for v_band in v_bands:
        for comparo in comparos:
            if "VJ1_VNP" in comparo:
                for tile in tiles:
                    png_dir = os.path.join(root_dir, tile, comparo, product, v_band + '/')
                    print(png_dir)
                    gif_dir = root_dir
                    gif_list = [file for file in os.listdir(png_dir) if file.endswith('.png')]
                    gif_list.sort()
                    images = []
                    for file_name in gif_list: images.append(imageio.imread(png_dir + file_name))
                    try:
                        imageio.mimsave(gif_dir + comparo + '_' + product  + '_' + tile + '_' + v_band + '.gif', images, 'GIF', duration=0.1)
                    except:
                        print('failed to make gif for {} {} {} {}'.format(comparo, product, tile, m_band))
