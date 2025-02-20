#!/usr/bin/env python3
#
# Simple tCam display program using matplotlib and TCam
#
#  Note: Useful palette values are 'twilight', 'twilight_shifted', 'hsv', 'ocean',
#   'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix'
#   'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar'
#

# 11/13/24, changing the file to collect image per second

import argparse
import array
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import time
import os
from tcam import TCam
from datetime import datetime

parser = argparse.ArgumentParser()

parser.prog = "disp_image"
parser.description = f"{parser.prog} - an example program to display image data from tCam\n"
parser.usage = "disp_image.py [--ip=<ip address of camera>] [--pl=<palette name>]"
parser.add_argument("-i", "--ip", help="IP address of the camera")
parser.add_argument("-p", "--pl", help="matplotlib image palette name")


if __name__ == "__main__":
    #
    # Parse command line
    #
    args = parser.parse_args()

    if not args.ip:
        ip = "192.168.4.1"
    else:
        ip = args.ip

    if not args.pl:
        palette = "CMRmap"
    else:
        palette = args.pl
    #
    # Open camera
    #
    cam = TCam(is_hw=True)
    stat = cam.connect()
    if stat["status"] != "connected":
        print(f"Could not connect to {ip}")
        cam.shutdown()
        sys.exit()

    

    # set up the save directory
    save_path = "/home/lab/tcam/tcam_images/"
    if not os.path.exists(save_path): 
        os.makedirs(save_path)  # if not, create a path

    # Time interval setup
    interval = 5  #time interval = 5s

    try: 
        while True: 
            #
            # Get image and decode radiometric data into an array of uint16 values
            #
            img_json = cam.get_image()
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
            a = np.zeros((120, 160, 3), np.uint8)
            for r in range(0, 120):
                for c in range(0, 160):
                    val = int((ra[(r * 160) + c] - imgmin) * 255 / delta)
                    if val > 255:
                        a[r, c] = [255, 255, 255]
                    else:
                        a[r, c] = [val, val, val]

            #
            # Slice into a single-color image so we can colorize it using a palette
            #
            lum_img = a[:, :, 0]

            #
            # Display
            #  Note: supported interpolation values are 'antialiased', 'none', 'nearest', 'bilinear',
            #   'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
            #   'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos', 'blackman'
            #
            plt.imshow(lum_img, interpolation="antialiased", cmap=palette)
            plt.colorbar()
            timestamp = time.time()
            readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            filename = f"tcam_image_{readable_time}.png"
            plt.savefig(os.path.join(save_path, filename)) # save image
            plt.show(block=False)  # will not stop, go rest code
            plt.pause(0.5)
            plt.clf() # clear all figures

            time.sleep(interval)

    except KeyboardInterrupt:
        print("Stopped by the user.")
    finally:
        cam.shutdown()

