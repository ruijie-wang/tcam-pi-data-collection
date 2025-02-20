# Tcam
This repository is designed to provide tutorials and basic code for setting up a tcam with a Raspberry Pi.
___
# Goals
1. [Intall system on Respberry Pi](#Install-system-on-ResPi)
2. [Python Code](#Python-Code)

3. Tricks
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
    * Type ```sudo nano cmdline.txt``` to edit the file from the path "_/boot/firmware/cmdline.txt_" add "_spidev.bufsiz=65536_" REMINDER:add this sentence in teh same line!

___
# Python Code
* Check examples from [Thermal Camera offical webpage](https://github.com/danjulio/tCam/tree/main/python)
* Codes in this repo
    * Read tjsn file and display as image using code named [Display_tjsn/tjsn_jpg.py](./Display%20tjsn/tjsn_jpg.py) 
    Reminder: ironblack.py file is needed!
    * Add date, temperature and humidity information on images using code named [Python_Code/addtempRH.py](./Python%20Code/addtempRH.py)