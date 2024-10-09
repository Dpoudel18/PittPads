# PittPads README

Group Members:

Yinuo Wang (AndrewID)
Libin Chen (AndrewID)
Lucas Huynh (lqh)
Dipesh Poudel (AndrewID)

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
-         conda activate your_environment_name

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
- The craigslist.py file is responsible for scraping data from Craigslist. The script only scrapes listings that include images to reduce the likelihood of scams.
- The scraped data will be saved as craigslist_apartments_final.csv in the src folder.
  
Please note that scraping Craigslist can take anywhere from 45 minutes to an hour.

For your convenience, pre-scraped data has already been provided in the src folder.

Step 2: Cleaning Data
- Once the scraping is complete, craigslist.py cleans the craigslist_apartments_final.csv file by dropping any rows with missing values in the following columns: name, zipcode, price, and location (address).
- The cleaned data will be written to a new CSV file named cleaned_cl_data.csv in a folder called data.
  
Again, for convenience, pre-cleaned data has been provided for you, as running craigslist.py can take up to an hour.

## Running the PittPads Application
To successfully run the PittPads application, please follow these instructions:

Set Your Working Directory: Ensure that your working directory is the src folder.

Source Code: The pittpads_streamlit.py file contains the source code for our application. It uses data from the data folder.

Running the Application: 

To run the application, open your terminal and type the following command:
- streamlit run pittpads_streamlit.py
- 
Do NOT simply run the code in VSCode or any other IDE.

Accessing the Application: After running the command, you will be taken to a localhost website where the application will be hosted.

Using the Filters: All filters are fully populated except for the zip code. To utilize all the features of our tools, please specify a zip code of your choosing.

DataFrame Functionalities: While most of the functions are self-explanatory, there are some cool features you can use with the DataFrames:
- You can press the arrow on a column name to sort the values from lowest to highest.
- You can also search for a particular listing you'd like to view.
  
Loading Images: The display image functionality may sometimes take a while to load. If you encounter issues loading images:
- Ensure that you have specified a zip code.
- Refresh the page if needed.
