import os
import re
from PIL import Image, ImageDraw, ImageFont

def extract_and_display_from_directory(input_directory, output_directory, fontsize=55):
    
    os.makedirs(output_directory, exist_ok=True) # make dirctory if not exist

    for file_name in os.listdir(input_directory):
        pattern = r"^(\d{4})(\d{2})(\d{2})_(\d{2})-(\d{2})-(\d{2})_(\d{2}\-\d{2})C_(\d{2}\-\d{2})rh.png" # match the file name format, this extension is .png
        match = re.match(pattern, file_name)
        if match: # extract info
            year, month, day = match.group(1), match.group(2), match.group(3)
            hour, minute, second = match.group(4), match.group(5), match.group(6)
            temperature = match.group(7).replace("-", ".") # replace "-" in the file name to "."
            humidity = match.group(8).replace("-", ".")

            date_time = f"{year}-{month}-{day} {hour}:{minute}:{second}"
            temp_humidity = f"Temperature: {temperature}°C, Humidity: {humidity}%"

            image_path = os.path.join(input_directory, file_name + "")
            output_path = os.path.join(output_directory, file_name + "")
            # Check exists
            if os.path.exists(image_path):
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)
                # Define font
                try:
                    font = ImageFont.truetype("arial.ttf", size=fontsize)
                except IOError:
                    font = ImageFont.load_default()

                # Define text positions
                text_position = (480, 160)  # data and time
                text_position2 = (480, 100)  # temp and hum

                draw.text(text_position, date_time, fill="black", font=font)
                draw.text(text_position2, temp_humidity, fill="black", font=font)

                image.save(output_path)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Image file not found for: {file_name}")

# main 
input_directory = input("Enter files path: ").replace("\\",  "/")
output_directory = input("Enter output folder path: ").replace("\\", "/")
extract_and_display_from_directory(input_directory, output_directory)
