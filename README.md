# Tcam
This repository is designed to provide tutorials and basic code for setting up a tcam with a Raspberry Pi.
___
# Goals
1. [Intall system on Respberry Pi](#Install-system-on-ResPi)
2. [Python Code](#Python-Code)
3. [Data Management](#Data-Management)

4. Tricks
    a. No hang up operation:<br>
    ```python
    Format: nohup python 'target script'
    
    Example: nohup python /home/lab/tcam/python/examples/tcam_tjgn.py
    ```
    
    b. Automatically Running after Reboot
    * Open terminal in respberry Pi
    ```
    sudo crontab -e
    ```
    * Add a new line
    ```python
    @reboot python 'target script'

    Example: @reboot python /home/lab/tcam/python/examples/tcam_tjsn.py

___
# Install system on ResPi
* Following the Respberry Pi [official webpage's](https://www.raspberrypi.com/software/) instruction to flash system. 
* Entering Respberry Pi system
    * In terminal, turn on SPI, URAT.
    ```sudo raspi-config```
    * Type ```sudo nano cmdline.txt``` to edit the file from the path "_/boot/firmware/cmdline.txt_" add "_spidev.bufsiz=65536_" REMINDER: 1. Add this sentence in the same line! 2. Do not leave space on either side of the equation symbol!

___
# Python Code
* Check examples from [Thermal Camera offical webpage](https://github.com/danjulio/tCam/tree/main/python)
* Codes in this repo
    * Read tjsn file and display as image using code named [Display_tjsn/tjsn_jpg.py](./Display%20tjsn/tjsn_jpg.py) 
    Reminder: ironblack.py file is needed!
    * Add date, temperature and humidity information on images using code named [Python_Code/addtempRH.py](./Python%20Code/addtempRH.py)
 
___
# Data Management
* Server:
    1. Each hour, download .tjsn files to temp folder
    2. Create tjsn zip archive, when download
    3. move "hh\YYYYMMDD_hh.zip" file synced folder
 
* Client: Each day, process all tCamFiles:
* Go to each tCamfolder, then go to each YYMMDD\hhfolder
* create png zip archive
* create CSV with hearder row(“DATE”,”TIME”,”TempC”,”RH%”)
* Then in same script:
    1. Add each tjsn to a zip archive
    2. Convert each tjsn to png and add to another zip archive
    3. Add new row to .csv file, YYYYMMDD,hh:mm:ss,T,RH

