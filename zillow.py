import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time 

# Define the headers to mimic a browser request
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'referer': 'https://www.zillow.com/pittsburgh-pa/rentals/'
}

# Function to retrieve property URLs from Zillow rental listings
def get_url():
    print("Collecting Zillow Property URL for Scraping.....")
    property_url = []
    # Loop through the first twelve pages of rental listings
    for page in range(1,21):
        # Make a request to the Zillow rental listings page
        data = requests.get(f'https://www.zillow.com/pittsburgh-pa/rentals/{page}_p', headers=header)
        soup = BeautifulSoup(data.text, "lxml")
        
        # Find all property card links
        property_links = soup.find_all('a', {'data-test': 'property-card-link'})
        for result in property_links:
            # Append each property's URL to the list
            link = result.get('href')
            if 'zillow.com' not in link:
                url_val = "zillow.com" + result.get('href')
            else:
                url_val = result.get('href')
            if url_val not in property_url:
                property_url.append(url_val)  
    print("\nCollected Zillow Property URL for Scraping! Reading for Scraping!\n")
    return property_url

# Function to scrape detailed data for each property
def zillow_data():
    all_info = []  # List to hold all property information
    property_urls = get_url()  # Get the list of property URLs

    print("\nZillow Data Extraction Started!\n")
    for url_link in property_urls:
        try:
            # Make a request to each property URL
            
            data = requests.get(f'https://{url_link}', headers=header)
            print(f'Extracted... https://{url_link}')
        except requests.exceptions.ConnectionError as e:
            print("Site not reachable (Rate Limit Issue)! Skip...  ", url_link)
            time.sleep(0.1)
            continue  # Skip to the next URL on connection error
        
        # Print the current URL being processed
        soup = BeautifulSoup(data.text, "lxml")

        # Find the JSON-LD script tag containing the property data
        json_ld = soup.find('script', type='application/ld+json')

        # Load the JSON data if available
        if json_ld:
            json_data = json.loads(json_ld.string)

            # Extract relevant information from the JSON data
            name = json_data['name']
            location = (json_data['address']['streetAddress'] + ", " +
                       json_data['address']['addressLocality'] + ", " +
                       json_data['address']['addressRegion'] + ", " +
                       json_data['address']['postalCode'])
            zip_code = json_data['address']['postalCode']
            price = json_data['offers']['lowPrice']
            latitude = json_data['geo']['latitude']
            longitude = json_data['geo']['longitude']
            beds = None
            baths = None
            size = None
            units = None
            phone = json_data.get('telephone', 'N/A')  
            description = json_data['description']
            amenity = json_data['amenityFeature']['name']
            image_url = json_data['image']
            property_url = 'https://zillow.com' + json_data['id']
            data_source = 'Zillow'
            all_info.append([price,name,location,zip_code,beds,baths,size,units,phone,image_url,property_url,latitude,longitude,description,amenity,data_source])

            time.sleep(0.1)
    print("\nZillow Data Extraction Completed!\n")
    # Create a DataFrame from the collected data
    df = pd.DataFrame(all_info, columns=["price", "name", "location", "zip_code", "beds", "baths", "size", "units", "phone", "image_url", "property_url", "latitude", "longitude", "description", "amenity", "data_source"])
    df.to_csv("data/cleaned_zillow_data.csv")
    return df

print(zillow_data())