# Zomato Review Scraper

This project is a Zomato review scraper that extracts review links and review data from Zomato using Selenium and BeautifulSoup. The project is divided into two modules:

1. **Link Scraper**: Uses Selenium to scrape Restaurants links from Zomato.
2. **Review Scraper**: Uses Requests and BeautifulSoup to extract and save the review data.

## Features

- Scrapes review links from Zomato restaurant pages.
- Extracts reviews from the scraped links and saves them in JSON format.
- Handles session management and retries for robust scraping.
- Detects duplicate review pages using MD5 hashing.

## Installation

1. **Microsoft Edge Webdriver**
- Download web driver from this [link](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads)
- Install all the necessary library from requirements.txt
```
pip install -r requirements.txt
```

## Usage
- Link Scraper

The link scraper uses Selenium to extract restaurant links from Zomato. To run the link scraper, use the following command:

```
python link_scraper.py
```

- Review Scraper

- The review scraper extracts reviews from the links obtained by the link scraper. To run the review scraper, use the following command:

```
python review_scraper.py 
```

- This will scrape the reviews from the links in the links.json file and save the reviews in a JSON format.

## Note
- Download and test the Web driver before running the code
