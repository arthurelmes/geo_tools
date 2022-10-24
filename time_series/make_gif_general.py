import imageio
import os
import sys
from glob import glob

in_dir = sys.argv[1]
out_name = sys.argv[2]

png_list = glob(in_dir + "/*.png")

png_list.sort()

gif_frames = []
for png in png_list:
    gif_frames.append(imageio.imread(png))

imageio.mimsave(out_name, gif_frames, 'GIF', duration=0.1)
