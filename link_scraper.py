import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys

def load_links_from_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_link_to_file(link, existing_links, file_name):
    if link not in existing_links:
        existing_links.append(link)
        with open(file_name, 'w') as f:
            json.dump(existing_links, f)
        return True
    return False

def main():

    if len(sys.argv) != 2:
        print("Usage: python script.py [search_term] (Use + as spaces)")
        sys.exit(1)

    search_term = sys.argv[1]
    file_name = search_term.replace('+', '_') + '.json'
    

    # Set up the browser (Google Chrome in this case)
    driver = webdriver.Chrome()

    # Go to the target URL
    url = f'https://duckduckgo.com/?q={search_term}&t=h_&iax=images&ia=images&iaf=size%3ALarge'
    driver.get(url)

    # Click on the first div with a class of "tile--img__media"
    tile = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.tile--img__media'))
    )
    tile.click()

    # Load existing links from the file
    existing_links = load_links_from_file(file_name)

    while True:
        try:
            # Get the link with the text of "View File"
            view_file_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'View File'))
            )

            # Save the link to the file if it's not already present
            link = view_file_link.get_attribute('href')
            if link not in existing_links:
                save_link_to_file(link, existing_links, file_name)

            # Click the <i> with a class of "js-detail-next"
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-detail-next'))
            )
            next_button.click()

            # Pause for a moment to let the page load
            sleep(1)

        except NoSuchElementException:
            # No more <i> to click, break the loop
            break

    # Close the browser
    driver.quit()

if __name__ == '__main__':
    main()
