'''
Function: 
Manually assign w0, w1, w2, w3, w4, and h0, h1, h2, h3 
and detect regions (w0, w1, h0, h1), (w1, w2, h0, h1), (w2, w3, h0, h1), (w3, w4, h0, h1), (w0, w4, h2, h3)
Comparing method is using average values compare to a manually set threshold. 

03032025: Update the code to use the date and time format as 'date: 11/24/2024 time: 11:43:26' instead of using hyphens('-').
'''
import argparse
import array
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
import numpy as np
import sys
import os
import json
import pandas as pd
from pathlib import Path

input_folder = Path(input('Enter input files folder path: ')).as_posix()

# input_folder = r"F:\OneDrive - University of Florida\General - Dairy Cow Thermal Camera Team\Tcam_Ruijie\Region_Detection\data\Files_tjsn"

def detect_cows(filepath, w0=0, w1=40, w2=80, w3=120, w4=160,
                          h0=0, h1=40, h2=60, h3=120):
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
    
    # Calculate AVG 
    # [width, height, channel], three channels have the same values
    z1 = a_f[h0:h1, w0:w1, 0]
    z2 = a_f[h0:h1, w1:w2, 0]
    z3 = a_f[h0:h1, w2:w3, 0]
    z4 = a_f[h0:h1, w3:w4, 0]
    z5 = a_f[h2:h3, w0:w4, 0]

    # Avg method
    z1_avg = np.mean(z1)
    z2_avg = np.mean(z2)
    z3_avg = np.mean(z3)
    z4_avg = np.mean(z4)
    z5_avg = np.mean(z5)

    return z1_avg, z2_avg, z3_avg, z4_avg, z5_avg

    
# Scan whole folder

# init result
results = [] 

for filename in os.listdir(input_folder):
    if filename.endswith('tjsn'):
        file_path = os.path.join(input_folder, filename)
        try: 
            z1, z2, z3, z4, z5 = detect_cows(filepath=file_path)
            print(f"zone 1: {z1}")
            print(f"zone 2: {z2}")
            print(f"zone 3: {z3}")
            print(f"zone 4: {z4}")
            print(f"zone 5: {z5}")
            print("\n")
            results.append([filename[5:15].replace('-','/'), filename[16:24].replace('-',':'), z1, z2, z3, z4, z5])
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Convert to dataframe and save
df = pd.DataFrame(results, columns=['Date', 'Time', 'Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5'])
output_csv_path = os.path.join(input_folder, "zone_results.csv")
df.to_csv(output_csv_path, index=False) # do not write the y index
