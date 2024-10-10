import pandas as pd
import streamlit as st
import math
import folium
import numpy as np
from folium import Icon
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

# Load the CSV files from 'data' folder

redfin_df = pd.read_csv('../data/redfin_pittsburgh_rental_complete.csv')
craigslist_df = pd.read_csv('../data/cleaned_cl_data.csv')
apartments_df = pd.read_csv('../data/cleaned_apartments_data.csv')
zillow_df = pd.read_csv('../data/cleaned_zillow_data.csv')
fair_market_rent_df = pd.read_csv('../data/fair_market_rent_pittsburgh_HUD.csv')


def distance_from_cmu(lat, lon):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    cmu_lat = math.radians(40.443336)
    cmu_lon = math.radians(-79.944023)
    lat = math.radians(lat)
    lon = math.radians(lon)
    
    # Difference in coordinates
    dlat = lat - cmu_lat
    dlon = lon - cmu_lon
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(cmu_lat) * math.cos(lat) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance

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
st.markdown(
    """
    <h1 style='text-align: center; font-size: 80px; color: red;'>Pitt
        <span style='color: grey;'>Pads</span>
    </h1>
        <p style='text-align: center; font-size: 16px;'>Developed by Yinuo Wang, Libin Chen, Lucas Huynh, and Dipesh Poudel</p>
    """, 
    unsafe_allow_html=True
)

# Filter Tools Title
st.markdown("<h1 style='color: red;'>Filter Tools</h1>", unsafe_allow_html=True)


st.subheader("List of All Properties")
st.write(f"Found {len(df)} properties")

# Price Filter
df = df[df['price'] <= 20000] # Filter out homes, only looking for apartments 
manual_price_min = st.sidebar.text_input("Minimum Budget", 0)  # Set default as sidebar's current min
manual_price_max = st.sidebar.text_input("Max Budget", int(df['price'].max()))  # Set default as sidebar's current max

# Convert manual input to integers and ensure they're valid
try:
    manual_price_min = int(manual_price_min)
    manual_price_max = int(manual_price_max)
except ValueError:
    st.sidebar.error("Please enter valid numbers for the price range")

# Apply the price filter based on manual input
if manual_price_min > manual_price_max:
    st.sidebar.error("Minimum budget cannot be greater than maximum budget")
else:
    price_filter = (manual_price_min, manual_price_max)

# Some variable type conversion
df['beds'] = df['beds'].replace(0, 'Studio')
df['beds'] = df['beds'].apply(lambda x: int(x) if isinstance(x, float) and not pd.isna(x) else x)
df['beds'] = df['beds'].replace('N/A', '').astype(str)
df['baths'] = df['baths'].replace('N/A', '').astype(str)

# Bed, Bath, and Data Source Filters
beds_filter = st.sidebar.multiselect("Number of Beds", options=sorted(df['beds'].unique()), default=list(df['beds'].unique()))
baths_filter = st.sidebar.multiselect("Number of Baths", options=sorted(df['baths'].unique()), default=list(df['baths'].unique()))
data_source_filter = st.sidebar.multiselect("Data Source", options=sorted(df['data_source'].unique()), default=list(df['data_source'].unique()))


# Filter by zip_code
df['zip_code'] = df['zip_code'].astype(str)
df['zip_code'] = df['zip_code'].str.replace(',', '', regex=False).str.replace('.0', '', regex=False)
df['zip_code'] = df['zip_code'].astype(int)

# Default to nearby CMU Zip Codes
zip_code_filter = st.sidebar.multiselect("Select Zip Code", options=df['zip_code'].unique(), default = [15213, 15217])


# Calculate distance from CMU
df['distance_from_CMU'] = df.apply(lambda row: distance_from_cmu(row['latitude'], row['longitude']), axis=1)

# # Showing entire database of listings
st.dataframe(df.reset_index(drop=True))

# Filter data based on user input
filtered_df = df[
    (df['price'].between(price_filter[0], price_filter[1])) &
    (df['beds'].isin(beds_filter)) &
    (df['baths'].isin(baths_filter)) &
    (df['zip_code'].isin(zip_code_filter)) &
    (df['data_source'].isin(data_source_filter))
]

# Display the filtered results
st.subheader("Apply your filter")
if len(filtered_df) == 0:
    st.write("Choose the zip code")
if len(filtered_df) != 0:
    st.write(f"Found {len(filtered_df)} properties")
st.dataframe(filtered_df.reset_index(drop=True))

# Average rent price on that zip code
if len(zip_code_filter) != 0:
    zip_codes_filtered = [str(elem) for elem in zip_code_filter]
    selected_zip_codes = fair_market_rent_df[fair_market_rent_df['zip_code'].isin(zip_codes_filtered)]
    st.subheader("Average rent price on that zip code")
    st.dataframe(selected_zip_codes)

# Streamlit app layout
st.subheader("Distance from CMU (km)")

# Filter for maximum distance
max_distance = st.slider("Select Maximum Distance from CMU (km)", 
                          min_value=0.0, 
                          max_value=10.0, 
                          value=2.0)  # Default value

# Filter the DataFrame based on the selected distance
distance_filtered_df = filtered_df[df['distance_from_CMU'] <= max_distance]

# Display the filtered DataFrame
st.write("Filtered Data (Distance ≤ {:.2f} km)".format(max_distance))
st.dataframe(distance_filtered_df.reset_index(drop=True))


cmu_lat = 40.443336  # Latitude of CMU
cmu_lon = -79.944023  # Longitude of CMU

# Create a folium map centered at CMU
m = folium.Map(location=[cmu_lat, cmu_lon], zoom_start=15)

# Function to extract address up to the first comma
def get_address(address):
    return address.split(',')[0]

df_cleaned = distance_filtered_df.dropna(subset=['location', 'latitude', 'longitude'])

# Add markers for each house in the DataFrame
for index, row in df_cleaned.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=get_address(row['location']),
        icon=Icon(icon='home', color='blue')
    ).add_to(m)

st.subheader("Apartments Near CMU")

# Display the map in Streamlit
st_data = st_folium(m, width=700, height=500)


# Optionally, display images of the properties
if st.checkbox("Show Property Images"):
    for index, row in filtered_df.iterrows():
        try:
            st.image(row['image_url'], caption=row['name'], use_column_width=True)
        except:
            pass

# Use machine learning create pricing predictor
st.markdown("<h1 style='color: grey;'>Analysis Tools</h1>", unsafe_allow_html=True)

df['beds'] = df['beds'].replace('Studio', np.nan)
df['size'] = df['size'].fillna('').astype(str).str.replace(',', '', regex=False)
df['size'] = pd.to_numeric(df['size'], errors='coerce')

# Drop rows with NaN values in key columns for predictor
df_ml = df.dropna(subset=['price', 'size', 'beds', 'baths'])

# Define features and target variable
features = df_ml[['size', 'beds', 'baths']]
target = df_ml['price']

# Create a pipeline with an imputer and the RandomForestRegressor
pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # You can choose 'median' or another strategy
    ('model', RandomForestRegressor())
])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Fit the model
pipeline.fit(X_train, y_train)

# Make predictions on the test set
predictions = pipeline.predict(X_test)

# Input form for new data
st.write("### Predict Rent Price")
try:
    size_input = st.number_input("Enter Size (sq ft)", min_value=0)
    beds_input = st.number_input("Enter Number of Beds", min_value=0)
    baths_input = st.number_input("Enter Number of Baths", min_value=0)
except ValueError:
    st.number_input.error("Please enter valid numbers.")

# Button to predict
if st.button("Predict"):
    new_data = pd.DataFrame({
        'size': [size_input],
        'beds': [beds_input],
        'baths': [baths_input]
    })

    # Make prediction
    predicted_price = pipeline.predict(new_data)[0]
    st.write(f"### Predicted Rent Price: ${predicted_price:,.2f}")

# Calculate average rent price per platform
avg_price_df = df.groupby('data_source')['price'].mean().reset_index()

# Specify colors for each data source
colors = ['green', 'blue', 'purple', 'red'] 

# Plotting
fig = px.bar(avg_price_df, 
             x='data_source', 
             y='price', 
             title='Average Rent Price Across Platforms',
             labels={'price': 'Average Rent Price ($)', 'data_source': 'Data Source'},
             color=avg_price_df['data_source'],
             color_discrete_sequence=colors)

# Remove the legend
fig.update_layout(showlegend=False)

# Show plot in Streamlit
st.subheader("Average Rent Price Across Different Platforms")
st.plotly_chart(fig)

# Remove listings without a longitude, latitude, or price
df_map_cleaned = df.dropna(subset=['latitude', 'longitude', 'price'])

# Create a base map
pittsburgh_map = folium.Map(location=[40.4406, -79.9959], zoom_start=12)  # Centered on Pittsburgh

# Prepare data for heatmap
heat_data = [[row['latitude'], row['longitude'], row['price']] for index, row in df_map_cleaned.iterrows()]

# Create a heatmap layer
HeatMap(heat_data, radius=15).add_to(pittsburgh_map)

# Save the map as an HTML file
pittsburgh_map.save('pittsburgh_rent_heatmap.html')

# Display the map
st.subheader("Rent Price Heatmap of Pittsburgh")
st.components.v1.html(pittsburgh_map._repr_html_(), height=500)