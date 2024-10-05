import requests

def get_pittsburgh_fmr(api_key):
    # Pittsburgh MSA code
    pittsburgh_cbsa_code = "METRO38300M38300"  # Using the provided code

    # Step 1: Get FMR data for Pittsburgh
    fmr_data_url = f"https://www.huduser.gov/hudapi/public/fmr/data/{pittsburgh_cbsa_code}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    fmr_response = requests.get(fmr_data_url, headers=headers)
    
    # Check for successful response
    if fmr_response.status_code != 200:
        print("Failed to retrieve FMR data:", fmr_response.status_code, fmr_response.text)
        return
    
    # Parse the JSON response
    fmr_data = fmr_response.json().get("data", {})
    
    # Display FMR data
    return fmr_data