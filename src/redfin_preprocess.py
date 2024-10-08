import pandas as pd
import numpy as np

file = 'redfin_pittsburgh_rental_complete.csv'

df = pd.read_csv(file, encoding='utf-8')

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

print(df['name'])

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


print(df)

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

df.to_csv('data_1006.csv', index=False)