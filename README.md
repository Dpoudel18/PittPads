# PittPads README

Group Members:

- Yinuo Wang (yinuowan)
- Libin Chen (libinc)
- Lucas Huynh (lqh)
- Dipesh Poudel (dpoudel)

## Prerequisites
Before running the project, ensure that you have the following installed:
- Anaconda (which includes Python)
- Ensure that you change your working directory to the src folder.

## Installation of Required Modules
This project requires the following Python modules:

- requests
- BeautifulSoup (from bs4)
- csv (part of the standard library)
- re (part of the standard library)
- json (part of the standard library)
- pandas
- time (part of the standard library)
- streamlit
- math (part of the standard library)
- folium
- numpy
- matplotlib
- plotly
- sklearn (scikit-learn)
- selenium

To install the necessary packages, follow these steps:
- Open Anaconda Prompt (or your terminal).
- Activate your conda environment (if applicable):

  `conda activate your_environment_name`

Install required packages using the following commands:
- pip install requests
- pip install beautifulsoup4
- pip install pandas
- pip install streamlit
- pip install folium
- pip install numpy
- pip install matplotlib
- pip install plotly
- pip install scikit-learn
- pip install selenium

Note: The csv, re, json, time, and math modules are part of Python’s standard library and do not require installation.

## Craigslist Scraping and Cleaning
Step 1: Scraping Data
- The `craigslist.py` file is responsible for scraping data from Craigslist. The script only scrapes listings that include images to reduce the likelihood of scams.
- The scraped data will be saved as `craigslist_apartments_final.csv` in the src folder.
  
Please note that scraping Craigslist can take anywhere from 45 minutes to an hour.

For your convenience, pre-scraped data has already been provided in the src folder.


Step 2: Cleaning Data
- Once the scraping is complete, `craigslist.py` cleans the craigslist_apartments_final.csv file by dropping any rows with missing values in the following columns: name, zipcode, price, and location (address).
- The cleaned data will be written to a new CSV file named `cleaned_cl_data.csv` in a folder called data.
  
Again, for convenience, pre-cleaned data has been provided for you, as running `craigslist.py` can take up to an hour.


## Zillow Scraping and Cleaning
Scraping and Cleaning Data
- The zillow.py file is responsible for scraping and cleaning data from Zillow. Due to rate limit imposed by Zillow, there are relatively few rows scraped for Zillow compared to other sources.
- The command to run the Zillow scraper is `python3 zillow.py`
- The scraped data will be saved as `data/cleaned_zillow_data.csv` in the data folder.
- The Streamlit application will be then reading the data from `cleaned_zillow_data.csv` file in the data folder.

## Redfin Scraping and Cleaning
- The redfin.py file is responsible for scraping and cleaning data from Redfin.
- Before scraping data, make sure install Selenium and Chromedriver, and change the path for ChromeDriver(line 71)
- The Redfin scaped and cleaned data will be written to a CSV file named `redfin_pittsburgh_rental_complete.csv` in a folder called data.

## Apartments.com Scraping and Cleaning

### Overview
The `apartments_scraper.py` script is responsible for scraping rental listings from **Apartments.com**, specifically targeting properties in Pittsburgh, PA. The script collects detailed information about each apartment, including pricing, address, number of bedrooms and bathrooms, and additional amenities. After scraping, the data is cleaned and written into a structured CSV file for further analysis or visualization.

### Scraping Process
The script utilizes **Selenium** to interact with the Apartments.com website and scrape property data from multiple pages (1-18). For each apartment, the script extracts key details such as:

- **Property Name**
- **Location (Address)**
- **Zip Code**
- **Price**
- **Number of Bedrooms and Bathrooms**
- **Size** (in square feet)
- **Phone Number**
- **Amenities**
- **Property URL**
- **Image URL**
- **Data Source** (Apartments.com)

### Cleaning Process
The scraped data is processed and cleaned by handling missing values and normalizing text data. Special handling is applied to ensure consistent extraction of fields like price, size, and zip codes using regular expressions.

### Output
Once the scraping is completed, the cleaned data is stored in a CSV file named `cleaned_apartments_data.csv` inside the `data` directory. The data can be used for analysis or visualization purposes.

### Running the Script

#### ChromeDriver Setup:
1. Download the appropriate version of **ChromeDriver** for your system.
2. Extract the file and note its path.
3. Update the `chrome_driver_path` variable in the script to point to the location of the ChromeDriver executable (line 12).

#### Execution:
After setting up ChromeDriver, you can run the script using the command below:

```bash
python apartments_scraper.py
```

### Output Location:
The scraped and cleaned data will be saved as `cleaned_apartments_data.csv` in the `data` folder.

### Example of Scraped Data Fields:
The CSV file will contain the following fields:

- **price**: Price of the apartment.
- **name**: Name or title of the property.
- **location**: Full address of the apartment.
- **zip_code**: Zip code of the property location.
- **beds**: Number of bedrooms in the apartment.
- **baths**: Number of bathrooms in the apartment.
- **size**: Size of the apartment in square feet.
- **units**: (Field not available on Apartments.com, included for potential future use).
- **phone**: Contact phone number for the property.
- **image_url**: URL of the main image of the apartment listing.
- **property_url**: URL of the apartment listing on Apartments.com.
- **latitude**: (Field not available, included for potential future use).
- **longitude**: (Field not available, included for potential future use).
- **description**: (Field not available, included for potential future use).
- **amenity**: List of amenities offered by the apartment.
- **data_source**: The source of the data (set to "Apartments.com").


## Running the PittPads Application
To successfully run the PittPads application, please follow these instructions:

Set Your Working Directory: Ensure that your working directory is the src folder.

Source Code: The `pittpads_streamlit.py` file contains the source code for our application. It uses data from the data folder.

Running the Application: 

To run the application, open your terminal and type the following command:

`streamlit run pittpads_streamlit.py`
  
Do NOT simply run the code in VSCode or any other IDE.

Accessing the Application: After running the command, you will be taken to a localhost website where the application will be hosted.

Using the Filters: All filters are fully populated except for the zip code. To utilize all the features of our tools, please specify a zip code of your choosing.

DataFrame Functionalities: While most of the functions are self-explanatory, there are some cool features you can use with the DataFrames:
- You can press the arrow on a column name to sort the values from lowest to highest.
- You can also search for a particular listing you'd like to view.
  
Loading Images: The display image functionality may sometimes take a while to load. If you encounter issues loading images:
- Ensure that you have specified a zip code.
- Refresh the page if needed.
