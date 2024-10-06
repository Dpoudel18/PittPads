from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to parse home listing data
def extract_data(soup):
    homes = soup.find_all('div', class_='HomeCardContainer')  # Find all home listings based on website structure
    data = []
    for home in homes:
        try:
            # Get the price
            price = home.find('span', class_='bp-Homecard__Price--value').text.strip()

            # Get the location
            location = home.find('div', class_='bp-Homecard__Address').text.strip()

            # Get home information
            beds = home.find('span', class_='bp-Homecard__Stats--beds').text.strip()
            baths = home.find('span', class_='bp-Homecard__Stats--baths').text.strip()
            size = home.find('span', class_='bp-Homecard__LockedStat--value').text.strip()
            # size = home.find('span', class_='bp-Homecard__Stats--sqft').text.strip()

            # Get the units info (e.g., "3 units")
            units = home.find('span', class_='KeyFacts-item').text.strip() if home.find('span', class_='KeyFacts-item') else 'N/A'

            # Get the phone number
            phone = 'N/A'
            button_labels = home.find_all('span', class_='ButtonLabel')
            for label in button_labels:
                if '(' in label.text and ')' in label.text:  # Check for parentheses to identify phone numbers
                    phone = label.text.strip()
                    break

            # Get the image URL if it exists
            image_tag = home.find('img', class_='bp-Homecard__Photo--image')
            if image_tag and 'src' in image_tag.attrs:
                image_url = image_tag['src']
            else:
                image_url = 'N/A'  # Set a default value if no image is found

            # Get the URL of the home listing
            home_url = home.find('a', class_='link-and-anchor visuallyHidden')['href']
            full_home_url = 'https://www.redfin.com' + home_url  # Construct the full URL

            # Save the extracted data in the list
            data.append({
                'Price': price,
                'Location': location,
                'Beds': beds,
                'Baths': baths,
                'Size': size,
                'Units': units,
                'Phone': phone,
                'Image_URL': image_url,
                'Home_URL': full_home_url
            })

        except AttributeError:
            # Skip listings that don't have complete information
            continue
    return data

# Set the path to ChromeDriver
chrome_driver_path = '/opt/homebrew/bin/chromedriver'
service = Service(chrome_driver_path)

# Using Chrome options
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Start ChromeDriver using Selenium 4 syntax
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Redfin Pittsburgh apartments-for-rent page with pagination
url = 'https://www.redfin.com/city/15702/PA/Pittsburgh/apartments-for-rent/page-'

all_data = []

# Loop through pages 1 to 9
for i in range(1, 10):
    driver.get(url + str(i))

    # Wait for the page to load
    time.sleep(3)

    # Scroll the page in increments
    scroll_pause_time = 1  # Pause time between each scroll (in seconds)

    scroll_increment = 400  # Scroll increment in pixels
    current_position = 0
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get the initial page height

    while current_position < last_height:
        # Scroll the page from the current position down by a certain pixel amount
        current_position += scroll_increment
        driver.execute_script(f"window.scrollTo(0, {current_position});")

        # Wait for the page to load
        time.sleep(scroll_pause_time)

        # Get the new page height
        new_height = driver.execute_script("return document.body.scrollHeight")

        last_height = new_height

        # If the current scroll position exceeds or reaches the total height, exit the loop
        if current_position >= last_height:
            break

    # Get the page HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all_data.extend(extract_data(soup))

df = pd.DataFrame(all_data)

print(df)

df.to_csv('redfin_pittsburgh_rental_complete.csv', index=False)

driver.quit()