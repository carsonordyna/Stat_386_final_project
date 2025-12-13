import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

url = 'https://raw.githubusercontent.com/sethfrand/Stat_386_final_project/refs/heads/main/data/test_data.csv'
df = pd.read_csv(url)

st.title("Utah Housing Data")

st.markdown("""
This application explains how to use the Utah Housing Data Package.

This project is a Python package designed to collect and analyze Utah housing data from UtahRealEstate.com.
It focuses on properties in Utah County and Salt Lake County, providing structured data as well as tools
for cleaning, visualization, and analysis.

The package web scraper uses
[Playwright](https://github.com/oxylabs/playwright-web-scraping)
for browser automation and easy integration into other Python projects.
""")

st.markdown("## Features")

st.markdown(
    """
| Feature | Description |
|--------|------------|
| Scraping | Scrapes housing listings for multiple cities in Utah |
| MLS Number | Extracts MLS listing numbers |
| Price | Listing price of the property |
| Address | Street address of the property |
| Beds / Baths / Sq Ft | Number of bedrooms, bathrooms, and square footage |
| Year Built | Year the property was built |
| Lot Size | Size of the property lot |
| Garage | Garage availability and size |
| Listing Agent | Agent responsible for the listing |
| Output Format | Exports data as a Pandas DataFrame or CSV file |
| Configurable Listings | Specify number of listings per city |
| Target Cities | Choose which Utah cities to scrape |
""")


st.markdown("## Package")

st.markdown("""
## **Package**

The main package is `utah_housing_stat386`, located in the
`src/utah_housing_stat386/` directory. It contains the core functionality
for scraping and data handling.

- **core.py**: Contains the main scraping logic and data processing functions  
- **__init__.py**: Initializes the package and exposes the `get_data` function

---

## **Installation**

1. **Install Playwright browsers** (required for scraping):
```
pip install playwright
playwright install
```
This will download the necessary browser binaries (Chromium, Firefox, WebKit) for Playwright.
""")



st.markdown("## Example")
st.markdown("""
Here is an example of how to use the package while using the the demo 
data that is available in the package.
""")

st.dataframe(df)