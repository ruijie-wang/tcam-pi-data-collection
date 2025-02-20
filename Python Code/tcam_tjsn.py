# 11/14/24 created, it used to collect tjsn files from TCam

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
        img = cam.get_image()
        json_data = json.dumps(img)
        timestamp = time.time()
        readable_time = datatime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        file_name = f"tcam_{readable_time}.tjsn"
        with open(os.path.join(save_path, file_name), 'w') as file:
            file.write(json_data)

        time.sleep(interval)

except KeyboardInterrupt:
    print("Stopped by the user.")
finally:
    cam.shutdown()