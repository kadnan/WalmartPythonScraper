from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json


# parse_page accepts html and page number and returns a list of records.
# Using Beautifulsoup library instead of Selenium for pasrsing as it is lighter and efficient
# and there is no need to keep heavy webdriver in memory while it is not needed.
def parse_page(html, pg_no=1):
    title = url = None
    position = overall_position = 0
    offset = 24 * (pg_no - 1)  # Each page has 24 records so offset for overall position is being calculated
    records = []
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.select('.Grid-col')

    for element in elements:  # Iterate each item
        title_section = element.select('.tile-title')  # extract title of the product
        url_section = element.select('a')  # extract url of the product
        if title_section:  # make sure that the title element exists
            title = title_section[0].text
        if url_section:  # make sure that the URL element exists
            url = url_section[0]['href']
        if title is not None:  # the first dom element returns empty, this check avoids to include it in list
            position += 1  # Increment position variable
            overall_position = position
            if pg_no > 1:  # If it is the page other than 1, overall position will be equal to offset and position sum
                overall_position = offset + position  # Calculating offset based position
            # Construct the JSON Payload of an individual product
            record = {'title': title, 'url': BASE_URL + url, 'position': position, 'overall_position': overall_position,
                      'page_no': pg_no}
            records.append(record)  # Append product in the array
    return records


""" 
    fetch takes a keyword and access the HTML of the page which is then passed to
    parse_page that generates JSON list of records
"""


def fetch(kw):
    overall_records = []
    page_no = 1
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    driver.get('https://www.walmart.com/store/5939-bellevue-wa/search?query={}'.format(kw))

    # We need to scroll down a bit so that we can click search button to fetch records
    driver.execute_script('window.scrollBy(0,600)')
    sleep(2)  # Delay for a while
    # click the search button
    driver.find_element_by_css_selector('.button-wrapper').click()
    sleep(5)
    driver.execute_script('window.scrollBy(0,500)')
    # Fetch the newly generated html
    html = driver.page_source
    overall_records.extend(parse_page(html))

    # Pagination, we will
    while page_no != TILL_PAGE_NO:
        page_no += 1
        # First we need to access the DOM of button, once found, scroll down to it to make it visible.
        pagination_element = driver.find_element_by_class_name('paginator-btn-next')
        driver.execute_script("arguments[0].scrollIntoView();", pagination_element)
        # Click the NEXT button
        driver.execute_script("arguments[0].click();", pagination_element)
        sleep(5)
        html = driver.page_source
        # store the JSON items in the array. At the end it will hold all items.
        overall_records.extend(parse_page(html, page_no))
    driver.quit()
    return overall_records


if __name__ == '__main__':
    TILL_PAGE_NO = 3  # constant that tell the number of pages to be accessed
    BASE_URL = 'https://www.walmart.com/'  # constant for the base Walmart URL
    CHROME_DRIVER_PATH = '/Users/AdnanAhmad/Data/Setups/chromedriver'  # constant for the Chrome Driver executable.
    result = fetch('tillamook')
    # store the results in JSON file
    with open('solution_2.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(result))
        print('Data successfully saved in solution_2.json')
