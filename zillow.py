# pip3 install lxml
# pip3 install requests
# pip3 install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time 

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        ,'referer':'https://www.zillow.com/pittsburgh-pa/rentals/'
          }

def get_url():
    property_url = []
    for page in range(2):
        data = requests.get(f'https://www.zillow.com/pittsburgh-pa/rentals/{page}_p', headers=header)
        soup = BeautifulSoup(data.text, "lxml")
        property_links = soup.find_all('a', {'data-test': 'property-card-link'})
        for result in property_links:
            property_url.append("zillow.com" + result.get('href'))  
    return property_url

def zillow_data():

    all_info = []
    property_url = get_url()

    for url_link in property_url:
        try:
            data = requests.get(f'https://{url_link}', headers=header)
        except requests.exceptions.ConnectionError:
            print("Site not rechable", url)
        print(f'https://{url_link}')
        soup = BeautifulSoup(data.text, "lxml")

        # Find the JSON-LD script tag
        json_ld = soup.find('script', type='application/ld+json')

        # Load the JSON data
        if json_ld:
            json_data = json.loads(json_ld.string)

        name = json_data['name']
        address = json_data['address']['streetAddress'] + ", " + json_data['address']['addressLocality'] + ", " + json_data['address']['addressRegion'] + ", " + json_data['address']['postalCode']
        zip_code = json_data['address']['postalCode']
        price = json_data['offers']['lowPrice']
        latitude = json_data['geo']['latitude']
        longitute = json_data['geo']['longitude']
        phone = json_data['telephone']
        description = json_data['description']
        amenity = json_data['amenityFeature']['name']
        image = json_data['image']
        url = 'https://zillow.com' + json_data['id']
        # name, address, zip_code, price, latitude, longitute, phone, description, amenity, image, url
        all_info.append([name, address, zip_code, price, latitude, longitute, phone, description, amenity, image, url])
        time.sleep(1)

    df = pd.DataFrame(all_info, columns = ["Name", "Address", "Zip_code", "Price", "Latitude", "Longitute", "Phone", "Description", "Amenity", "Image", "Url"]) 
    return df

# def zillow_data():
#     property_name = []
#     addr = []
#     pr = []
#     property_url = []
#     bed = []

#     for page in range(2):
#         data = requests.get(f'https://www.zillow.com/pittsburgh-pa/rentals/{page}_p', headers=header)
#         soup = BeautifulSoup(data.text, "lxml")
#         address = soup.find_all('address', {'data-test':'property-card-addr'})
#         price = soup.find_all('span', {'data-test':'property-card-price'})
#         property_links = soup.find_all('a', {'data-test': 'property-card-link'})
#         try:
#             beds = soup.find_all('span', {'class' : 'Text-c11n-8-102-0__sc-aiai24-0 PropertyCardInventoryBox__BedText-srp-8-102-0__sc-1jotqb7-2 bhZlvi hZrLIt'})
#         except:
#             beds = ""

#         for result in address:
#             try:
#                 if "|" in result.text:
#                     property_name.append(result.text.split("|")[0])
#                 else:
#                     property_name.append("")
#                 addr.append(result.text.split("|")[1])
#             except:
#                 addr.append(result.text)

#         for result in price:
#             pr.append(result.text)   

#         for result in property_links:
#             property_url.append("zillow.com" + result.get('href'))   

#         for i, result in enumerate(beds):
#             try:
#                 bed.append(result.text)   
#             except:
#                 bed.append("")

#     big_row = list(zip(property_name, addr, pr, property_url))

#     df = pd.DataFrame(big_row, columns = ['Property Name', 'Address', 'Price', 'Property Link']) 

#     df.to_csv("demo.csv", index=False)

#     return df

# print(zillow_data())