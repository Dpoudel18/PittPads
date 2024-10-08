from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import re

# Set the path to your ChromeDriver
chrome_driver_path = "/Users/dipeshpoudel/downloads/chromedriver-mac64/chromedriver"
service = Service(chrome_driver_path)

# Initialize Chrome browser
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment this line to run in headless mode
driver = webdriver.Chrome(service=service, options=options)

# Function to get text from multiple possible selectors
def get_element_text(apt, selectors):
    for selector in selectors:
        try:
            element = apt.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except NoSuchElementException:
            pass
    return None

# Function to get attribute from multiple possible selectors
def get_element_attribute(apt, selectors, attribute):
    for selector in selectors:
        try:
            element = apt.find_element(By.CSS_SELECTOR, selector)
            return element.get_attribute(attribute)
        except NoSuchElementException:
            pass
    return None

# Create a list to store all apartments' information
apartment_list = []

# Loop through all 18 pages
for page_number in range(1, 19):
    if page_number == 1:
        url = 'https://www.apartments.com/pittsburgh-pa/'
    else:
        url = f'https://www.apartments.com/pittsburgh-pa/{page_number}/'

    print(f"Processing page {page_number}: {url}")

    # Open the target URL
    driver.get(url)

    # Wait for the apartment listings to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.mortar-wrapper')))

    # Get all actual apartment list items
    apartments = driver.find_elements(By.CSS_SELECTOR, 'li.mortar-wrapper')

    # Iterate over each apartment and extract data
    for index, apt in enumerate(apartments, start=1):
        # Initialize variables
        price = None
        name = None
        location = None
        zip_code = None
        beds = None
        baths = None
        size = None
        units = None  # Not available
        phone = None
        image_url = None
        property_url = None
        latitude = None  # Not available
        longitude = None  # Not available
        description = None  # Not available
        amenity = None
        data_source = 'Apartments.com'

        # Extract property title
        property_title = get_element_text(apt, [
            'div.property-title',
            'p.property-title',
            'div.property-title-wrapper .property-title',
            'div.property-information a.property-link .property-title',
            'div.property-wrapper .property-title-wrapper .property-title'
        ])
        name = property_title if property_title else 'N/A'

        # Extract address
        property_address = get_element_text(apt, ['div.property-address', 'p.property-address'])
        if not property_address:
            # Try to get address from data-streetaddress attribute
            try:
                article_element = apt.find_element(By.TAG_NAME, 'article')
                street_address = article_element.get_attribute('data-streetaddress')
                if street_address:
                    property_address = street_address
                else:
                    property_address = None
            except NoSuchElementException:
                property_address = None

        # If address is still incomplete, try to extract from property title
        if not property_address or not re.search(r'\b[A-Za-z]{2}\b \d{5}$', property_address):
            # Check if property title contains the full address
            if ',' in property_title:
                property_address = property_title.strip()
            else:
                property_address = None

        location = property_address if property_address else 'N/A'

        # Extract zip code from address
        if property_address:
            zip_code_match = re.search(r'\b\d{5}(?:-\d{4})?\b', property_address)
            if zip_code_match:
                zip_code = zip_code_match.group(0)
            else:
                zip_code = None
        else:
            zip_code = None

        # Extract price and process it to get the maximum price
        property_pricing = get_element_text(apt, [
            'p.property-pricing',
            'p.property-rents',
            'div.price-range',
            'div.property-information-wrapper .price-range'
        ])
        if property_pricing:
            # Remove any non-numeric characters except for hyphens and periods
            pricing_numbers = re.findall(r'\d+[,]*\d*', property_pricing.replace(',', ''))
            if pricing_numbers:
                prices = [int(price) for price in pricing_numbers]
                price = max(prices)
            else:
                price = None
        else:
            price = None

        # Extract beds, baths, and size
        property_beds = get_element_text(apt, [
            'p.property-beds',
            'div.bed-range',
            'div.property-information-wrapper .bed-range'
        ])
        if property_beds:
            # Extract beds, baths, and size using regex
            beds_match = re.search(r'(\d+)\s*Beds?', property_beds, re.IGNORECASE)
            baths_match = re.search(r'(\d+(?:\.\d+)?)\s*Baths?', property_beds, re.IGNORECASE)
            size_match = re.search(r'([\d,]+)\s*sq\s*ft', property_beds, re.IGNORECASE)

            beds = int(beds_match.group(1)) if beds_match else None
            baths = float(baths_match.group(1)) if baths_match else None
            size = int(size_match.group(1).replace(',', '')) if size_match else None
        else:
            beds = None
            baths = None
            size = None

        # Extract amenities
        amenities_tags = apt.find_elements(By.XPATH, ".//p[@class='property-amenities']//span")
        amenities_list = []
        for amenity in amenities_tags:
            full_text = amenity.get_attribute('title') or amenity.get_attribute('aria-label') or amenity.get_attribute('textContent').strip()
            amenities_list.append(full_text)
        amenity = ', '.join(amenities_list) if amenities_list else ''

        # Extract phone number
        phone_number = get_element_text(apt, ['a.phone-link', 'a.phone-link.js-phone'])
        phone = phone_number if phone_number else ''

        # Extract property link
        property_link = get_element_attribute(apt, ['a.property-link'], 'href')
        property_url = property_link if property_link else 'N/A'

        # Extract image link
        image_link = get_element_attribute(apt, [
            'div.carousel-inner div.carousel-item.active img',
            'div.media img',
            'div.media-inner img',
            'div.imageContainer img',
            'div.imageContainer .carousel-inner .carousel-item.active img'
        ], 'src')
        image_url = image_link if image_link else ''

        # Print each apartment's information to the console
        print(f"Page {page_number} - Apartment {index}")
        print(f"Name: {name}")
        print(f"Location: {location}")
        print(f"Zip Code: {zip_code}")
        print(f"Price: {price}")
        print(f"Beds: {beds}")
        print(f"Baths: {baths}")
        print(f"Size: {size}")
        print(f"Units: {units}")
        print(f"Phone: {phone}")
        print(f"Image URL: {image_url}")
        print(f"Property URL: {property_url}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Description: {description}")
        print(f"Amenity: {amenity}")
        print(f"Data Source: {data_source}")
        print('-' * 40)

        # Add the information to the list
        property_info = {
            'price': price if price is not None else '',
            'name': name,
            'location': location,
            'zip_code': zip_code if zip_code is not None else '',
            'beds': beds if beds is not None else '',
            'baths': baths if baths is not None else '',
            'size': size if size is not None else '',
            'units': units if units is not None else '',
            'phone': phone,
            'image_url': image_url,
            'property_url': property_url,
            'latitude': latitude if latitude is not None else '',
            'longitude': longitude if longitude is not None else '',
            'description': description if description is not None else '',
            'amenity': amenity,
            'data_source': data_source
        }

        apartment_list.append(property_info)

# Save to CSV file with the specified format
fieldnames = [
    'price',
    'name',
    'location',
    'zip_code',
    'beds',
    'baths',
    'size',
    'units',
    'phone',
    'image_url',
    'property_url',
    'latitude',
    'longitude',
    'description',
    'amenity',
    'data_source'
]

with open('data/cleaned_apartments_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for apt_info in apartment_list:
        writer.writerow(apt_info)

print('Information successfully extracted and saved to cleaned_apartments_data.csv.')

# Close the browser
driver.quit()
