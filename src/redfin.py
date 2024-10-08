from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

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

# df.to_csv('redfin_pittsburgh_rental_complete.csv', index=False)

driver.quit()

file = 'redfin_pittsburgh_rental_complete.csv'

# df = pd.read_csv(file, encoding='utf-8')

# Remove all non-numeric characters (except for the decimal point) from the 'Price' column
df['Price'] = df['Price'].str.replace(r'[^\d.]', '', regex=True)
df = df[df['Price'] != '']

# Convert the cleaned 'Price' column to integers
df['Price'] = pd.to_numeric(df['Price']).astype(int)

# df['name'] = df['Location'].apply(lambda x: x.split('|')[0].strip() if '|' in x else '')
# Get names from url
df['name'] = df['Home_URL'].apply(lambda x: x.split('/')[-3].strip() if 'unit' not in x else x.split('/')[-4].strip())
df['name'] = df['name'].str.replace('-', ' ')
df['name'] = df['name'].str.replace(r'(\d{5})$', '', regex=True)


df['Location'] = df['Location'].apply(lambda x: x.split('|')[1].strip() if '|' in x else x)

# Split the 'Location' column into 'Zipcode' using regex
df['zip_code'] = df['Location'].str.extract(r'(\d{5})$')

# print(df['name'])

# Function to clean bed and bath values
def clean_beds_baths(value, col_name):
    if pd.isna(value):
        return np.nan
    value = str(value)
    if 'Beds' in col_name:
        # Handle 0 beds as Studio
        if '0' in value:
            return 'Studio'
        # Extract the lower range if it's a range
        if '-' in value:
            return value.split('-')[0].strip()
        # Handle the case when it's not a range
        return value.split(' ')[0].strip()
    if 'Baths' in col_name:
        # Extract the lower range if it's a range
        if '-' in value:
            return value.split('-')[0].strip()
        # Handle the case when it's not a range
        return value.split(' ')[0].strip()
    return value

# Function to clean size values
def clean_size(value):
    if pd.isna(value) or value == '—':
        return np.nan
    value = str(value)
    # Check for various dash types and extract lower range of size
    if '-' in value:
        return value.split('-')[0].strip().replace(',', '')  # Removing commas from size ranges
    # Handle the case when it's a single value
    return value.strip()


df['Beds'] = df['Beds'].apply(lambda x: clean_beds_baths(x, 'Beds'))
df['Baths'] = df['Baths'].apply(lambda x: clean_beds_baths(x, 'Baths'))
df['Size'] = df['Size'].apply(clean_size)


df['description'] = df['Units'].apply(lambda x: str(x) if 'unit' not in str(x) or 'Laundry' in str(x) else '')

df['Units'] = df['Units'].apply(lambda x: x.split(' ')[0].strip() if 'unit' in str(x) and 'Laundry' not in str(x) else '')

df = df.rename(columns={
    'Home_URL': 'property_url',
    'Image_URL': 'image_url',
    'name': 'name',
    'Location': 'location',
    'Price': 'price',
    'Beds': 'beds',
    'Baths': 'baths',
    'Size': 'size',
    'Units': 'units',
    'Phone': 'phone',
    'zip_code': 'zip_code',
    'description': 'description'
})

df['latitude'] = np.nan
df['longitude'] = np.nan
df['amenity'] = np.nan
df['data_source'] = 'redfin'

df = df.reindex(columns=[
    'name', 'location', 'price', 'zip_code', 'beds', 'baths', 'size',
    'units', 'phone', 'image_url', 'property_url', 'latitude',
    'longitude', 'description', 'amenity', 'data_source'
])

df.to_csv(file, index=False)