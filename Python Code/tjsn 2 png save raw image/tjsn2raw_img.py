# %%
'''
Only save the raw image(160 by 120) from converting TJSN file
'''
import argparse
import array
import base64
import matplotlib.pyplot as plt
import matplotlib as mpl
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


# Define function to read and process tjsn file
def process_tjsn_file(filepath, temp_mode): 
    with open(filepath, 'r') as file:
        img_json = json.load(file) # Load JSON content

    dec_rad = base64.b64decode(img_json["radiometric"])
    ra = array.array('H', dec_rad)
    
    # Calcualte the normal temperature
    a = np.zeros((120,160,3), float) # Celsius
    a_f = np.zeros((120,160,3), float) # Fahrenheit
    for r in range(0,120):
        for c in range(0,160):
            val = ((ra[(r * 160) + c]/100)-273.15)
            val_f = (val * 9/5) + 32
            a[r,c] = [val,val,val]
            a_f[r,c] = [val_f, val_f, val_f]

    # select which temperature mode
    if temp_mode == 'F':
        lum_img = a_f[:,:,0]
        vmin = 50 # C = 10
        vmax = 90 # C = 32.2
        output_path = os.path.join(output_folder, os.path.basename(filepath).replace('.tjsn', '.png')) # output path
        plt.imsave(output_path, lum_img, cmap=ironblack_colormap) # save img only

        # Plot and save with colorbar(only)
        colorbar_path = os.path.join(output_folder, "F_colorbar.png")
        # Create a dummy ScalarMappable for the colorbar
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)  # normalized value to cover all color
        sm = mpl.cm.ScalarMappable(cmap=ironblack_colormap, norm=norm)
        sm.set_array([])  # Needed for colorbar to work

        # Plot and save only the colorbar
        fig, ax = plt.subplots(figsize=(1, 6))  # Adjust size as needed
        cb = plt.colorbar(sm, cax=ax, orientation='vertical', label=f'Temperature (°{temp_mode})')
        fig.savefig(colorbar_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

    if temp_mode == 'C':
        lum_img = a[:,:,0]
        vmin = 10 # C = 10
        vmax = 32.2 # C = 32.2

        # Save raw thermal image 
        output_path = os.path.join(output_folder, os.path.basename(filepath).replace('.tjsn', '.png'))
        plt.imsave(output_path, lum_img, cmap=ironblack_colormap) # save img only

        # Plot and save with colorbar
        colorbar_path = os.path.join(output_folder, "C_colorbar.png")
        # Create a dummy ScalarMappable for the colorbar
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)  # normalized value to cover all color
        sm = mpl.cm.ScalarMappable(cmap=ironblack_colormap, norm=norm)
        sm.set_array([])  # Needed for colorbar to work

        # Plot and save only the colorbar
        fig, ax = plt.subplots(figsize=(1, 6))  # Adjust size (width by height)
        cb = plt.colorbar(sm, cax=ax, orientation='vertical', label=f'Temperature (°{temp_mode})')
        fig.savefig(colorbar_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)



if __name__ == "__main__":
    # Define input and output folder
    input_folder = input('Enter input files folder path: ')
    input_folder = input_folder.replace("\\", "/")   # \\ means \ character
    output_folder = input('Enter output folder path: ')
    output_folder = output_folder.replace("\\", "/")
    while True:
        Temp_unit = input('Enter display temperature unit (C or F): ').strip().upper()
        if Temp_unit in ['C', 'F']:
            break
        print("Invalid input. Please enter 'C' for Celsius or 'F' for Fahrenheit.")

    # Chech the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Scan folder
    for filename in os.listdir(input_folder):
        if filename.endswith('tjsn'):
            file_path = os.path.join(input_folder, filename)
            try: 
                process_tjsn_file(filepath=file_path, temp_mode=Temp_unit)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
# %%
