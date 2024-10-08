import requests
from api_key import API_KEY
import pandas as pd

api_key = API_KEY

def get_pittsburgh_fmr():
    """
    This function retrieves and returns Fair Market Rent (FMR) data 
    for the Pittsburgh Metropolitan Statistical Area using a provided API key.
    """
    # Pittsburgh MSA code
    pittsburgh_cbsa_code = "METRO38300M38300"  # Using the provided code

    # Step 1: Get FMR data for Pittsburgh
    fmr_data_url = f"https://www.huduser.gov/hudapi/public/fmr/data/{pittsburgh_cbsa_code}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    fmr_response = requests.get(fmr_data_url, headers=headers)
    
    # Check for successful response
    if fmr_response.status_code != 200:
        print("Failed to retrieve FMR data:", fmr_response.status_code, fmr_response.text)
        return
    
    # Parse the JSON response
    fmr_data = fmr_response.json().get("data", {})
    
    # Display FMR data
    df = pd.DataFrame(fmr_data["basicdata"])
    df.to_csv("data/fair_market_rent_pittsburgh_HUD.csv", index = False)
    return fmr_data

print(get_pittsburgh_fmr())