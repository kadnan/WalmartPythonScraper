import time
import requests
from selenium import webdriver
from time import sleep
import json


# This function will use Selenium browser to fetch cookies generated via Javascript
# and then these cookies are passed in request library again and again
def get_cookies(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    with webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options) as driver:
        driver.get('https://www.walmart.com/store/5939-bellevue-wa/search?query='.format(
            keyword))  # Though hardcoded word could work but it is fine to make things genuine as much as possible
        time.sleep(10)
        driver_cookies = driver.get_cookies()
        cookie = {c['name']: c['value'] for c in driver_cookies}
    return cookie


# parse accepts a JSON structure and returns the list of product in JSON format.
# When the page number is given it access the JSON structure of that page number.
def parse(data, pg_no=1):
    position = 0
    records = []
    overall_position = 0
    offset = 24 * (pg_no - 1)  # Each page has 24 records so offset for overall position is being calculated

    # Extracts the list of items
    items = data['itemStacks'][0]['items']
    for item in items:
        if position > 23:  # Because on page it shows only 24 items, rest are extra and not rendered
            break
        title = item['title']  # Extracting title
        url = BASE_URL + item[
            'productPageUrl']  # Extracting relative product page URL which is then glued with BASE_URL
        position += 1  # Increment Position
        overall_position = position
        if pg_no > 1:  # If it is the page other than 1, overall position will be equal to offset and position sum
            overall_position = offset + position  # Calculating offset based position

        # Construct the JSON Payload of an individual product
        record = {'title': title, 'url': BASE_URL + url, 'position': position, 'overall_position': overall_position,
                  'page_no': pg_no}
        records.append(record)  # Append product in the array
    return records


def fetch(keyword, cookies, pg_no=1):
    page_no = 1
    overall_records = []
    headers = {  # Setting initial headers to be passed.
        'authority': 'www.walmart.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'content-type': 'application/json',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.walmart.com/store/5939-bellevue-wa/search?query=tillamook',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    }

    with requests.session() as session:
        while page_no != TILL_PAGE_NO + 1:  # need one extra iteration as it skips first time on my machine, may be IP flagged suspicious
            params = (
                ('query', keyword),
                ('stores', '5939'),
                ('cat_id', '0'),
                ('ps', '24'),
                ('offset', 24 * (page_no - 1)),
                # Each page has 24 records so offset is calculated to go to the next page
                ('prg', 'desktop'),
                ('zipcode', '98006'),
                ('stateOrProvinceCode', 'WA'),
            )
            r = session.get(
                'https://www.walmart.com/store/electrode/api/search',
                params=params,
                headers=headers,
                cookies=cookies
            )
            if r.status_code == 200:  # to check HTTP status code
                result = r.json()  # Fetch the JSON payload
                records = parse(result, page_no)  # Send the Payload for products listing extraction.
                overall_records.extend(records)  # Save the listings in array.
                page_no += 1
            sleep(3)  # To avoid blocking
    return overall_records


if __name__ == '__main__':
    kw = 'tillamook'
    # constant that tell the number of pages to be accessed. Unlike other solutions
    # The 4 is set here because cookies are not set at first iteration and it is skipping
    # so we have to run 4 iteration to fetch 3 pages
    TILL_PAGE_NO = 3
    BASE_URL = 'https://www.walmart.com/'  # constant for the base Walmart URL
    CHROME_DRIVER_PATH = '/Users/AdnanAhmad/Data/Setups/chromedriver'
    site_cookies = get_cookies(kw)
    output = fetch(kw, site_cookies)
    # store the results in JSON file
    with open('solution_3.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(output))
        print('Data successfully saved in solution_3.json')
