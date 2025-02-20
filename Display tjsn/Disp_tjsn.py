import argparse
import array
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
import numpy as np
import sys
import os
# from tcam import TCam
import json
from ironblack import ironblack_palette

# Setting the customized color map
# Normalize RGB values to the range [0, 1] for matplotlib
ironblack_palette_normalized = np.array(ironblack_palette) / 255.0
# Create the ListedColormap
ironblack_colormap = mcolors.ListedColormap(ironblack_palette_normalized, name="ironblack")


# Read the file
with open('./raw_files/tcam_2024-11-25 03-06-17.tjsn', 'r') as file:
    img_json = json.load(file)  # Parse JSON content

dec_rad = base64.b64decode(img_json["radiometric"])
ra = array.array('H', dec_rad)
#
# Determine minimum/maximum 16-bit values in radiometric data
#
imgmin = 65535
imgmax = 0

for i in ra:
    if i < imgmin:
        imgmin = i
    if i > imgmax:
        imgmax = i

delta = imgmax - imgmin
print(f"Max val is {imgmax}, Min val is {imgmin}, Delta is {delta}")

#
# Linearize 16-bit data within range imgmin/imgmax to an 8-bit image
#
# a = np.zeros((120, 160, 3), np.uint8)
# for r in range(0, 120):
#     for c in range(0, 160):
#         val = int((ra[(r * 160) + c] - imgmin) * 255 / delta)
#         if val > 255:
#             a[r, c] = [255, 255, 255]
#         else:
#             a[r, c] = [val, val, val]

# Customized measurement CLSIUS
a = np.zeros((120,160,3), float) # Celsius
a_f = np.zeros((120,160,3), float) # Fahrenheit
for r in range(0,120):
    for c in range(0,160):
        val = ((ra[(r * 160) + c]/100)-273.15)
        val_f = (val * 9/5) + 32
        a[r,c] = [val,val,val]
        a_f[r,c] = [val_f, val_f, val_f]
#
# Slice into a single-color image so we can colorize it using a palette
#
lum_img = a_f[:, :, 0]

# Value range based on calculation
# vmin = np.min(a_f)
# vmax = np.max(a_f)

# Manually Value range
vmin = 50
vmax = 90

#
# Display
#  Note: supported interpolation values are 'antialiased', 'none', 'nearest', 'bilinear',
#   'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
#   'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos', 'blackman'
#
im = plt.imshow(lum_img, interpolation="antialiased", cmap=ironblack_colormap,
                vmin=vmin, vmax=vmax)
# Add the colorbar
cbar = plt.colorbar(im)
cbar.set_label('Fahrenheit')
intervals = np.arange(vmin,vmax, 5) # interval is 1 
if vmax not in intervals:
    intervals = np.append(intervals, vmax)
cbar.set_ticks(intervals)  # Show only the min and max values
cbar.ax.set_yticklabels([f'{val:.1f}' for val in intervals])  # Format labels
# plt.colorbar()
plt.show()