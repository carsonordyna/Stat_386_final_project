
# **STAT 386 Final Project: Utah Housing Data Scraper**

## **Overview**

This project is a Python package designed to collect and analyze Utah housing data from UtahRealEstate.com. It focuses on properties in **Utah County** and **Salt Lake County**, providing structured data as well as tools for cleaning, visualization, and analysis.

The package's web scraper uses **Playwright** for browser automation and easy integration into other Python projects.

***

## **Features**

*   Scrapes housing listings for multiple cities in Utah
*   Extracts details such as:
    *   MLS number
    *   Price
    *   Address
    *   Beds, Baths, Square Footage
    *   Year Built, Lot Size, Garage
    *   Listing Agent
*   Outputs data as:
    *   **Pandas DataFrame** or
    *   **CSV file**
*   Configurable:
    *   Number of listings per city
    *   Target cities

***

## **Project Structure**

    Stat_386_final_project/
    ├── LICENSE
    ├── README.md
    ├── data/
    │   ├── Salt_Lake_County_housing_data.csv
    │   ├── test_data.csv
    │   └── utah_housing_data_ORIGINAL.csv
    ├── pyproject.toml
    ├── scripts/
    │   ├── _scraper_less_intensive.py
    │   ├── salt_lake_county.py
    │   └── scraper.py
    ├── src/
    │   └── utah_housing_stat386/
    │       ├── __init__.py
    │       └── core.py
    └── uv.lock

***

## **Package**

The main package is `utah_housing_stat386`, located in the `src/utah_housing_stat386/` directory. It contains the core functionality for scraping and data handling.

*   `core.py`: Contains the main scraping logic and data processing functions
*   `__init__.py`: Initializes the package and exposes the `get_data` function

***

## **Installation**

1.  **Install Playwright browsers** (required for scraping):
    ```bash
    pip install playwright
    playwright install
    ```
    This will download the necessary browser binaries (Chromium, Firefox, WebKit) for Playwright.

***

## **Usage**

The main functionality is exposed via the `get_data` function in `utah_housing_stat386.core`.

### **Example**

```python
from utah_housing_stat386 import get_data

# Fetch data for all cities, 5 listings per city, return as DataFrame
df = get_data(max_listings=5, output="pandas")
print(df.head())

# Save data to CSV
get_data(max_listings=10, output="csv")
```

***

## **Configuration**

*   **max\_listings**: Number of listings per city (default: 5)
*   **cities**: List of cities (default: all supported cities)
*   **output**: `"pandas"` DataFrame or `"csv"` file (default: `"pandas"`)

Supported cities include:

*   **Utah County**: alpine, american-fork, eagle-mountain, highland, lindon, lehi, orem, provo, saratoga-springs, spanish-fork
*   **Salt Lake County**: draper, holladay, midvale, millcreek, cottonwood-heights, murray, salt-lake-city, sandy, south-jordan, south-salt-lake, sugarhouse, west-jordan, west-valley

***

## **Data Files**

*   `data/utah_housing_data_ORIGINAL.csv`: Sample of scraped data for Utah County
*   `data/Salt_Lake_County_housing_data.csv`: Sample of scraped data for Salt Lake County
*   `data/test_data.csv`: Test dataset (produced in development)

## **Scripts (produced in development)**

*  `scripts/scraper.py`: Main scraper script using Playwright
*  `scripts/_scraper_less_intensive.py`: Less intensive version of the scraper
*  `scripts/salt_lake_county.py`: Script to scrape Salt Lake County data

## **Other Files**

*  `pyproject.toml`: Project configuration and dependencies
*  `uv.lock`: Lock file for dependencies
*  `requirements.txt`: List of required Python packages
*  `setup.py`: Setup script for packaging

***

## **Data Cleaning**

The package includes comprehensive data cleaning functions to transform raw scraped data into analysis-ready format.

### **Quick Start with Cleaned Data**
```python
from utah_housing_stat386 import get_cleaned_data

# Get cleaned data directly
df_clean = get_cleaned_data(max_listings=10, output="pandas")
print(df_clean.head())
```

### **Manual Cleaning Workflow**
```python
from utah_housing_stat386 import get_data, clean_housing_data, remove_duplicates, remove_invalid_rows

# Get raw data
df_raw = get_data(max_listings=10)

# Apply cleaning step-by-step
df_clean = clean_housing_data(df_raw)
df_clean = remove_duplicates(df_clean)
df_clean = remove_invalid_rows(df_clean)
```

### **Individual Cleaning Functions**
```python
from utah_housing_stat386 import clean_price, clean_lot_size, clean_agent

# Clean specific fields
df['price'] = df['price'].apply(clean_price)
df['lot_size'] = df['lot_size'].apply(clean_lot_size)  # Converts to acres
df['agent'] = df['agent'].apply(clean_agent)  # Removes contact info
```

### **Cleaning Functions Reference**

| Function | Description | Example Input | Example Output |
|----------|-------------|---------------|----------------|
| `clean_price()` | Converts price strings to numeric | "$481,999" | 481999.0 |
| `clean_numeric_field()` | Cleans beds, baths, sqft | "1,252" | 1252.0 |
| `clean_year_built()` | Validates year built | "1919" | 1919 |
| `clean_lot_size()` | Converts to acres | "0.10 Ac" | 0.1 |
| `clean_garage()` | Extracts garage spaces | "2" | 2 |
| `clean_agent()` | Removes contact info | "Contact Agent John Doe 801-555-1234" | "John Doe" |
| `clean_city()` | Standardizes city names | "salt-lake-city" | "Salt Lake City" |
| `clean_housing_data()` | Applies all cleaning | DataFrame | Cleaned DataFrame |
| `remove_duplicates()` | Removes duplicate listings | DataFrame | Deduplicated DataFrame |
| `remove_invalid_rows()` | Removes rows with missing critical data | DataFrame | Filtered DataFrame |

## **License**

MIT 2025

***
