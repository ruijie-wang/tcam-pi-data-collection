# 11/14/24 created, it used to collect tjsn files from TCam
# WRJ updated 12/21/24 based on Dr. Hofstetter added TEMP+HUM.
    # Change content include: added subfolder for each hour; changed save file name.
# DWH updated 12/24/24 to make /H subfolders and replace the decimals with - no symbols
# WRJ: save the tjsn file directly into .zip file. e.g tjsn_collection/20250520/01.zip
#                                                                              /02.zip
#                                                                              /....


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
import json
import smbus2
import bme280
import zipfile

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

cam = TCam(is_hw=True)
stat = cam.connect()
if stat["status"] != "connected":
    print(f"Could not connect to chipboard")
    cam.shutdown()
    sys.exit()

# check the dir, if not create one
save_path = "/home/lab/tcam/tjsn_collection/"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# set time interval
interval = 5 # 5 seconds

try:
    while True:
        img = cam.get_image()  # obtain the image
        json_data = json.dumps(img)

        # Read sensor data
        temperature_celsius,pressure,humidity = bme280.readBME280All()

        # Convert temperature to Fahrenheit
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

        # Print the readings
        print("Temperature: {:.2f} °C, {:.2f} °F".format(temperature_celsius, temperature_fahrenheit))
        print("Pressure: {:.2f} hPa".format(pressure))
        print("Humidity: {:.2f} %".format(humidity))

        # Save the file
        timestamp = time.time()
        readable_time = datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H-%M-%S') # change to format like "YYYYMMDD_hh-mm-ss"
        date_hour = datetime.fromtimestamp(timestamp).strftime("%Y%m%d/%H") # save the hour string was "%Y%m%d_%H"  looks like 20250521/14

        # # Create subfolder for each new hour
        # subfolder_path = os.path.join(save_path, date_hour) # concatnate the original path and the hour name
        # if not os.path.exists(subfolder_path):
        #     os.makedirs(subfolder_path)

        # Substitute subfolder to zip folder
        zip_folder_path = os.path.join(save_path, os.path.dirname(date_hour))  # /tjsn_collection/20250521/
        if not os.path.exists(zip_folder_path):  # check if exist
            os.makedirs(zip_folder_path)

        zip_file_path = os.path.join(save_path, f"{date_hour}.zip")  # Create a void zip file e.g 20250521/14.zip

        temp_celsius_str = "{:.2f}C".format(temperature_celsius).replace('.', '-') # save the temperature celsius string
        humidity_str = "{:.2f}rh".format(humidity).replace('.', '-') # save the humidity string


        file_name = f"{readable_time}_{temp_celsius_str}_{humidity_str}.tjsn"  # change to format like "YYYYMMDD_hh-mm-ss_temperature_humidity"
        # with open(os.path.join(subfolder_path, file_name), 'w') as file:
        #     file.write(json_data)
        # print(f"{file_name} has been successful written in {subfolder_path}")

        # append file into a zip file
        with zipfile.ZipFile(zip_file_path, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:   # append mode, zip deflate compression method
            zf.writestr(file_name, json_data)

        print(f"{file_name} has been added to {zip_file_path}")

        time.sleep(interval)

except KeyboardInterrupt:
    print("Stopped by the user.")
finally:
    cam.shutdown()