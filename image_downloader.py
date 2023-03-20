import os
import json
import urllib.request
import shutil

# The folder containing the JSON files
input_folder = 'image_links'
downloaded_folder = 'downloaded'

# Create the "downloaded" folder if it doesn't exist
os.makedirs(downloaded_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        # Create a folder with the same name as the JSON file (excluding the extension)
        output_folder = os.path.join(input_folder, filename[:-5])
        os.makedirs(output_folder, exist_ok=True)

        # Read the JSON file
        with open(os.path.join(input_folder, filename), 'r') as json_file:
            image_links = json.load(json_file)

        # Download and save the images
        for idx, image_url in enumerate(image_links):
            try:
                # Download the image
                response = urllib.request.urlopen(image_url, timeout=10)

                # Save the image with a sequential number in the output folder
                # and prepend the JSON file name (excluding the extension)
                image_filename = f'{filename[:-5]}_image_{idx + 1}.jpg'
                with open(os.path.join(output_folder, image_filename), 'wb') as image_file:
                    image_file.write(response.read())

                print(f'Downloaded image {idx + 1} from {filename}')
            except Exception as e:
                print(f'Error downloading image {idx + 1} from {filename}: {e}')

        # Move the JSON file to the "downloaded" folder
        shutil.move(os.path.join(input_folder, filename), os.path.join(downloaded_folder, filename))
