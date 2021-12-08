# Walmart Scraper

This repo contains the code of Walmart scrapers. There are 3 different solutions:

## Setup

Assuming Python is installed, run the command `pip install -r requirements.txt`.

### Solution 1

Solution 1 is the script written in python using `requests` library. This script is passing the header and query strings
fetched from the URL's headers. This script is passing the hardcoded cookie. It generates a JSON file with
name `solution_1.json`
The script took **8.1 seconds** with **3% CPU usage** on my machine. In order to run, execute, `python3 solution_1.py`

### Solution 2

This solution is pure Selenium based, it creates headless browser instance to access the page. There is no cookie issue
since it is visiting in headless . It generates file with name `solution_2.json`
Ths script took **31.58 seconds**  with **8% CPU usage** on my machine. In order to run,
execute, `python3 solution_2.py`

### Solution 3

This solution is hybrid, it is using both Selenium and Python requests library. It uses Selenium instance to fetch
javascript generated cookies and then those cookies are passed to `requests` library in iteration. The script took **8.1
seconds** with **4% CPU usage** on my machine. In order to run, execute, `python3 solution_3.py`

## About JSON fields
The JSON structure of an individual product looks like below:
```
{
    "title": "Tillamook All Natural Teriyaki Beef Jerky",
    "url": "https://www.walmart.com/https://www.walmart.com//ip/Tillamook-All-Natural-Teriyaki-Beef-Jerky/420598755",
    "position": 24,
    "overall_position": 72,
    "page_no": 3
  }
```
- title:- Product name
- url: The URL of the individual product
- position: position of product within a page.
- overall_position: The overall position of the entry across pages.