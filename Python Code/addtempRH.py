# This code takes a data.csv file with date, time, tempF, humidity and assigns the temp/RH values
# to files within the time range then adds text to each image
import csv
from PIL import Image, ImageDraw, ImageFont
import os
import cv2

# Initialize arrays
months = []
days = []
years = []
hours = []
minutes = []
seconds = []
temps = []
humidities = []

# Read the CSV file
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Split date and time
        date_parts = row['Date'].split('/')
        time_parts = row['Time'].split(':')
        
        # Append data to respective arrays
        months.append(int(date_parts[0]))
        days.append(int(date_parts[1]))
        years.append(int(date_parts[2]))
        hours.append(int(time_parts[0]))
        minutes.append(int(time_parts[1]))
        seconds.append(int(time_parts[2]))
        temps.append(float(row['Temperature']))
        humidities.append(float(row['Humidity']))

def add_text_to_image(folder_path, output_path):
    """Parses the filename, extracts text, and adds it to the image."""

    # Get all image file names in the folder
    images = [img for img in os.listdir(folder_path) if img.endswith((".png", ".jpg",".JPG", ".jpeg"))]
    images.sort()  # Ensure images are in the correct order    

    if not images:
        print("No images found in the specified folder.")
        return

    # Read the first image to get its dimensions
    first_image_path = os.path.join(folder_path, images[0])
    first_image = cv2.imread(first_image_path)
    height, width, _ = first_image.shape
    print("image size height and width = ", height, width)

    # Add each image to the video
    for image_name in images:
        image_path = os.path.join(folder_path, image_name)

        # Parse filename
        filename = image_path.split('/')[-1]  # Get filename from path
        print(f"FILENAME = {filename}")
        date_txt = filename.split('_')[-1].split(" ")[0]
        print(f"date_txt = {date_txt}")
        time_txt = filename.split(' ')[-1].split("png")[0]
        year = date_txt.split('-')[0]
        month = date_txt.split('-')[1]
        day = date_txt.split('-')[2]
        hh = time_txt.split('-')[0]
        mm = time_txt.split('-')[1]
        ss = time_txt.split('-')[2]
        print(f"ss = {ss}")

        # Find the corresponding temperature and humidity values
        temp = None
        humidity = None
        for i in range(len(years) - 1):
            print(f"{months[i]}-{days[i]}-{years[i]} {hours[i]}:{minutes[i]}:{seconds[i]}")
            print(f"{month}-{day}-{year} {hh}:{mm}:{ss}")
            print(f"{months[i]}-{days[i]}-{years[i]} {hours[i+1]}:{minutes[i+1]}:{seconds[i+1]}")
            if (years[i] == int(year) and months[i] == int(month) and days[i] == int(day) and 
                hours[i] <= int(hh) and int(hh) <= hours[i+1] and 
                minutes[i] <= int(mm) and int(mm) <= minutes[i+1]):
#and 
#                seconds[i] <= int(ss) and int(ss) <= seconds[i+1]):
                temp = temps[i]
                humidity = humidities[i]
                break

        if temp is None or humidity is None:
            print(f"No matching data found for {filename}")
            continue

        # Open the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Choose a font
        font = ImageFont.truetype("arial.ttf", 36)  # Replace with your desired font

        # Add text to the image
        text_to_add = f"{month}-{day}-{year} {hh}:{mm}:{ss} Temp: {temp}F Humidity: {humidity}%"
        draw.text((480, 160), text_to_add, font=font, fill=(255, 0, 0))

        # Save the modified image
        out_path = os.path.join(output_path, image_name)
        print(f"outpath = {out_path}")
        img.save(out_path)

# Define input and output folder
input_folder = input('Enter input files folder path: ')
input_folder = input_folder.replace("\\", "/")   # \\ means \ character
output_folder = input('Enter output folder path: ')

add_text_to_image(folder_path= input_folder, 
                  output_path= output_folder)