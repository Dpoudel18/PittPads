import pandas as pd
import streamlit as st

# Load the CSV files

redfin_df = pd.read_csv('data/cleaned_redfin_data.csv')
craigslist_df = pd.read_csv('data/cleaned_cl_data.csv')
apartments_df = pd.read_csv('data/cleaned_apartments_data.csv')
zillow_df = pd.read_csv('data/cleaned_zillow_data.csv')
fair_market_rent_df = pd.read_csv('data/fair_market_rent_pittsburgh_HUD.csv')

# Define the consistent column order
column_order = [
    'price', 'name', 'location', 'zip_code', 'beds', 'baths', 
    'size', 'units', 'phone', 'image_url', 'property_url', 
    'latitude', 'longitude', 'description', 'amenity', 'data_source'
]

# Reindex each DataFrame to ensure they have the same columns

redfin_df = redfin_df.reindex(columns=column_order)
craigslist_df = craigslist_df.reindex(columns=column_order)
zillow_df = zillow_df.reindex(columns=column_order)

# Combine the DataFrames
df = pd.concat([zillow_df, redfin_df, craigslist_df, apartments_df], ignore_index=True)

# Streamlit app title
st.title("List of All Properties!")
st.write(f"Found {len(df)} properties")

# Filter by price
price_filter = st.sidebar.slider("Price Range", 0, int(df['price'].max()), (0, int(df['price'].max())))

# Filter by beds, baths, data_source
df['beds'] = df['beds'].replace('N/A', '').astype(str)
df['baths'] = df['baths'].replace('N/A', '').astype(str)
beds_filter = st.sidebar.multiselect("Number of Beds", options=sorted(df['beds'].unique()), default=list(df['beds'].unique()))
baths_filter = st.sidebar.multiselect("Number of Baths", options=sorted(df['baths'].unique()), default=list(df['baths'].unique()))
data_source_filter = st.sidebar.multiselect("Data Source", options=sorted(df['data_source'].unique()), default=list(df['data_source'].unique()))

# Show all the listings
st.dataframe(df)

# Filter by zip_code
zip_code_filter = st.sidebar.multiselect("Select Zip Code", options=df['zip_code'].unique())

# Filter data based on user input
filtered_df = df[
    (df['price'].between(price_filter[0], price_filter[1])) &
    (df['beds'].isin(beds_filter)) &
    (df['baths'].isin(baths_filter)) &
    (df['zip_code'].isin(zip_code_filter)) &
    (df['data_source'].isin(data_source_filter))
]

# Display the filtered results
st.subheader("Apply your filter!")
if len(filtered_df) == 0:
    st.write("Choose the zip code")
if len(filtered_df) != 0:
    st.write(f"Found {len(filtered_df)} properties")
st.dataframe(filtered_df)

# Average rent price on that zip code
if len(zip_code_filter) != 0:
    zip_codes_filtered = [str(elem) for elem in zip_code_filter]
    selected_zip_codes = fair_market_rent_df[fair_market_rent_df['zip_code'].isin(zip_codes_filtered)]
    st.subheader("Average rent price on that zip code!")
    st.dataframe(selected_zip_codes)

# Optionally, display images of the properties
if st.checkbox("Show Property Images"):
    for index, row in filtered_df.iterrows():
        try:
            st.image(row['image_url'], caption=row['name'], use_column_width=True)
        except:
            pass