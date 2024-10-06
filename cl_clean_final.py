import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('craigslist_apartments_final.csv')

# Create a function to extract zip code from the address
def extract_zip_code(address):
    if isinstance(address, str):  # Check if the address is a string
        match = re.search(r'\b\d{5}\b', address)
        return int(match.group()) if match else None
    return None  # Return None if the address is not a string

def clean_price(price):
    # Convert price to string first if it's not NaN
    if pd.notna(price):
        price_str = str(price)
        # Remove non-digit characters (e.g., $, commas) from the string
        price_str = re.sub(r'[^\d]', '', price_str)
        # Return the cleaned price as an integer if it's a valid digit
        return int(price_str) if price_str.isdigit() else None
    return None  # Return None if the price is NaN or invalid

df['Price'] = df['Price'].apply(clean_price)

# Transform the data
df_cleaned = pd.DataFrame({
    'price': df['Price'].fillna(0).astype(int),
    'name': df['Name'].fillna(''),
    'location': df['Address'].fillna(''),
    'zip_code': df['Address'].apply(extract_zip_code),
    'beds': df['Bedrooms'].fillna(0).astype(int),
    'baths': df['Bathrooms'].fillna(0).astype(float),
    'size': pd.to_numeric(df['Sq. Footage'], errors='coerce').fillna(0).astype(float),
    'units': None,
    'phone': None,
    'image_url': None,
    'property_url': df['Link to Listing'].fillna(''),
    'latitude': df['Latitude'],
    'longitude': df['Longitude'],
    'description': None,
    'amenity': df[['Rent Period', 'Laundry', 'Parking']].fillna('').agg(', '.join, axis=1),
    'data_source': 'craigslist'
})

# Filter rows where the essential columns are non-null
df_cleaned = df_cleaned.dropna(subset=['price', 'name', 'location', 'zip_code', 'property_url'])

# Save the cleaned data to a new CSV
df_cleaned.to_csv('cleaned_cl_data.csv', index=False)
