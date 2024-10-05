from average_rent_by_zip import get_pittsburgh_fmr
from zillow import zillow_data
import pandas as pd
import streamlit as st

data_json = get_pittsburgh_fmr("")
data = pd.DataFrame(data_json['basicdata'])

# Title of the app
st.title("Neighborhood Information by Zip Code")

# Select a zip code from the dropdown
zip_code = st.selectbox("Select a Zip Code:", data)

# Display the information
st.write(f"### Information for Zip Code: {zip_code}")
df_zip_code = data[data['zip_code'] == zip_code].iloc[0]
st.write(df_zip_code)

st.write(f"### Zillow Data")
df_zillow_data = zillow_data()
st.write(df_zillow_data)

