# Deepfake project

## What it does now:
- *link_scraper.py*:
    - `python3 link_scraper.py [Image+Search]`
    - Creates a list of image links from duckduckgo and saves it to a json
- image_downloader:
    - `python3 image_downloader.py`
    - Looks at a folder called image_links and loops over every json file donwloading all the image links and saving the images in a folder with the same name as the json file 