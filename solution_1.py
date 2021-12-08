"""

"""
import json

import requests
from time import sleep


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


""" 
    fetch takes a keyword and access the HTML of the page which is then passed to
    parse() that generates JSON list of records
"""


def fetch(keyword):
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
        'cookie': 'brwsr=3546b2d8-4454-11ec-8b5a-dbae802bd5ca; ACID=3e3752b6-a706-4ddf-95a2-ae88083ebe3e; hasACID=true; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsInN0b3JlSW50ZW50IjoiUElDS1VQIiwibWVyZ2VGbGFnIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjMwODEiLCJ0aW1lc3RhbXAiOjE2MzY3ODg5MDEyMTB9LCJwb3N0YWxDb2RlIjp7InRpbWVzdGFtcCI6MTYzNjc4ODkwMTIxMCwiYmFzZSI6Ijk1ODI5In0sInZhbGlkYXRlS2V5IjoicHJvZDp2MjozZTM3NTJiNi1hNzA2LTRkZGYtOTVhMi1hZTg4MDgzZWJlM2UifQ%3D%3D; vtc=T0u0KwKFJGHeU3asnYGQ_w; TBV=7; DL=94066%2C%2C%2Cip%2C94066%2C%2C; TB_Latency_Tracker_100=1; TB_Navigation_Preload_01=1; crumb=2RJK-XnGcnZ8WeLbzMNhC6uSY75Q9sqHRkR8eVTWjyH; tb_sw_supported=true; TB_SFOU-100=1; AID=wmlspartner%253Dimp_150372%253Areflectorid%253Dimp_zl3TTEwhgxyIUNGVPPU0LViWUkGxlaWkqz2KVY0%253Alastupd%253D1638813128173; locDataV3=eyJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3siYnVJZCI6IjAiLCJub2RlSWQiOiIzMDgxIiwiZGlzcGxheU5hbWUiOiJTYWNyYW1lbnRvIFN1cGVyY2VudGVyIiwibm9kZVR5cGUiOiJTVE9SRSIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6Ijk1ODI5IiwiYWRkcmVzc0xpbmUxIjoiODkxNSBHZXJiZXIgUm9hZCIsImNpdHkiOiJTYWNyYW1lbnRvIiwic3RhdGUiOiJDQSIsImNvdW50cnkiOiJVUyIsInBvc3RhbENvZGU5IjoiOTU4MjktMDAwMCJ9LCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6MzguNDgyNjc3LCJsb25naXR1ZGUiOi0xMjEuMzY5MDI2fSwiaXNHbGFzc0VuYWJsZWQiOnRydWUsInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZX1dLCJkZWxpdmVyeSI6eyJidUlkIjoiMCIsIm5vZGVJZCI6IjMwODEiLCJkaXNwbGF5TmFtZSI6IlNhY3JhbWVudG8gU3VwZXJjZW50ZXIiLCJub2RlVHlwZSI6IlNUT1JFIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiOTU4MjkiLCJhZGRyZXNzTGluZTEiOiI4OTE1IEdlcmJlciBSb2FkIiwiY2l0eSI6IlNhY3JhbWVudG8iLCJzdGF0ZSI6IkNBIiwiY291bnRyeSI6IlVTIiwicG9zdGFsQ29kZTkiOiI5NTgyOS0wMDAwIn0sImdlb1BvaW50Ijp7ImxhdGl0dWRlIjozOC40ODI2NzcsImxvbmdpdHVkZSI6LTEyMS4zNjkwMjZ9LCJpc0dsYXNzRW5hYmxlZCI6dHJ1ZSwic2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwidW5TY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJhY2Nlc3NQb2ludHMiOlt7ImFjY2Vzc1R5cGUiOiJERUxJVkVSWV9BRERSRVNTIn1dfSwic2hpcHBpbmdBZGRyZXNzIjp7ImxhdGl0dWRlIjozOC40NzM4LCJsb25naXR1ZGUiOi0xMjEuMzQzOSwicG9zdGFsQ29kZSI6Ijk1ODI5IiwiY2l0eSI6IlNhY3JhbWVudG8iLCJzdGF0ZSI6IkNBIiwiY291bnRyeUNvZGUiOiJVU0EiLCJnaWZ0QWRkcmVzcyI6ZmFsc2V9LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjMwODEiLCJkaXNwbGF5TmFtZSI6IlNhY3JhbWVudG8gU3VwZXJjZW50ZXIiLCJhY2Nlc3NQb2ludHMiOm51bGwsImludGVudCI6IlBJQ0tVUCIsInNjaGVkdWxlRW5hYmxlZCI6ZmFsc2V9LCJpbnN0b3JlIjpmYWxzZSwicmVmcmVzaEF0IjoxNjM4ODM0NzI4MjkxLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6M2UzNzUyYjYtYTcwNi00ZGRmLTk1YTItYWU4ODA4M2ViZTNlIn0%3D; assortmentStoreId=3081; hasLocData=1; akavpau_p2=1638813728~id=0ddec06ac25050953645a4b5d72af4f0; adblocked=true; com.wm.reflector="reflectorid:imp_zl3TTEwhgxyIUNGVPPU0LViWUkGxlaWkqz2KVY0@lastupd:1638813132000@firstcreate:1636788901158"; next-day=null|true|true|null|1638862621; location-data=94066%3ASan%20Bruno%3ACA%3A%3A0%3A0|21k%3B%3B15.22%2C46y%3B%3B16.96%2C1kf%3B%3B19.87%2C1rc%3B%3B23.22%2C46q%3B%3B25.3%2C2nz%3B%3B25.4%2C2b1%3B%3B27.7%2C4bu%3B%3B28.38%2C2er%3B%3B29.12%2C1o1%3B%3B30.14|2|7|1|1xun%3B16%3B0%3B2.44%2C1xtf%3B16%3B1%3B4.42%2C1xwj%3B16%3B2%3B7.04%2C1ygu%3B16%3B3%3B8.47%2C1xwq%3B16%3B4%3B9.21; TB_DC_Flap_Test=0; bstc=cqPOkDdcHRbOOWnXljFUXU; mobileweb=0; xpa=; xpm=3%2B1638862621%2BT0u0KwKFJGHeU3asnYGQ_w~%2B0; _pxhd=1wGn8vPC/xYO43oIyZQIBmYn28J4J4/ceMd-WLk8e9M7Qyw0ToljNcm1zXiFNAC5tYcUXy88tg3nBqpdAuT5sQ==:dW/JtmJPPeYviWr1RnbGL8Q8fvsAnk/Tr319tYqmCEF-ZACrf9lbi8vQzvzKY6lDVRH5k5dW2zRPEnPwSFdhe9v-Q1NOMHusjxvPvQ2BFeM=; ak_bmsc=DEAF5D13B7E5DB9D1445A42C981F72DB~000000000000000000000000000000~YAAQP54QApQE/i99AQAATg3Tkw6GGZisOY9WqflSzzYhEOPbRvefmAkpiEYorVwUfg9UEAFnLY8StjWnjYCXsEqzFDDy+gnGpbydgZS+20l+VJJigKU51o2xuF8AJrgY5QzJhLMA/i9MxW5MRL+n0zV+BC1PLTb1hhelYx8GmmyDV+HifGBSgErgNtb6pUA5ydONX9EprYpZknQfqP30OmVWTnKkloTrQDkfJcJ0vI+P/MEZb8U2molWz/GdGwU+rbhcdSfa9oWaLaAp8E/DZjsY6YpmW4fmZNQTrUfa7P2db8EDnbWF1zi8r3D+51o2Hi7bd5Bi+8txdaDdl9YT3+Nr4VofqwkH5iXqOmidTDd/fO6qvtQyO0oau3Vjowa+xhn04TYYtlQjsb9A; xptwg=3271574160:209D26905C6B780:55789D4:D6539E2E:8EBD026C:E7FE99FF:; TS01b0be75=01538efd7c206a0dc58225169e0b825676e9c5e453ca7af568232e9be3e84e5a6227c4b728ed7713e869287e81ef2d29326fcd6cab; TS013ed49a=01538efd7c206a0dc58225169e0b825676e9c5e453ca7af568232e9be3e84e5a6227c4b728ed7713e869287e81ef2d29326fcd6cab; bm_mi=01610934A8DDD8546E2A0DEF61A8C91C~xOaPkjLqDDIuv11EPeZ1gIxvBQt6PD6zjA7Gd2qVQfVC6cwGG83ojqAvWCSM6IYwVuSjWY3iSyJNH7YzUX2nmRtIlmJUlrAz5tz3OU9v1zqnhHdq0QcCuMve0SUoKRpLcqWK65ocd9vpQR78SbT7CLWkBDckK4ro0g38t1cdBsBb8OZKF21D+M5ZU1pHVEuO3MvvWCWNDByoMpg9KcRVvq/67Rbu6fVBemqGJU3g54VcLF6BgDysyAiM1zrC5dHyOznoyGKalanQZpuh4hQQwg==; bm_sv=FA70A3C0284440D78F7D26E1C9316BD3~G6MyGle3ACdP7loWuTml7iej+WW4evzORtt1IKVCT/tduzxQYcbTI2Ti1xyqDnz8l6K0ty4wXsRVwrzTkcnDAzku7y4AVIZ5cKsSt9rThXIHazknmtE9Y0OSWFRz8IdFFrO5uHnXxAPnXTdp97vj7fYje/wT3m+GfZhmesPZZNs=',
    }
    params = (  # Query string parameters
        ('query', keyword),
        ('stores', '5939'),
        ('cat_id', '0'),
        ('ps', '24'),
        ('offset', '0'),
        ('prg', 'desktop'),
        ('zipcode', '98006'),
        ('stateOrProvinceCode', 'WA'),
    )
    # Establish a session
    session = requests.session()
    r = session.get(
        'https://www.walmart.com/store/electrode/api/search',
        params=params,
        headers=headers,
    )

    if r.status_code == 200:
        result = r.json()  # Extract the JSON payload
        records = parse(result)  # Send the JSON payload to parse to extract products
        overall_records.extend(records)

    # Access till page no 3
    while page_no != TILL_PAGE_NO:
        page_no += 1
        params = (
            ('query', keyword),
            ('stores', '5939'),
            ('cat_id', '0'),
            ('ps', '24'),
            ('offset', 24 * (page_no - 1)),  # Each page has 24 records so offset is calculated to go to the next page
            ('prg', 'desktop'),
            ('zipcode', '98006'),
            ('stateOrProvinceCode', 'WA'),
        )
        r = session.get(
            'https://www.walmart.com/store/electrode/api/search',
            params=params,
            headers=headers,
        )
        if r.status_code == 200:  # to check HTTP status code
            result = r.json()  # Fetch the JSON payload
            records = parse(result, page_no)  # Send the Payload for products listing extraction.
            overall_records.extend(records)  # Save the listings in array.
        sleep(3)  # To avoid blocking
    return overall_records


if __name__ == '__main__':
    TILL_PAGE_NO = 3  # constant that tell the number of pages to be accessed
    BASE_URL = 'https://www.walmart.com/'  # constant for the base Walmart URL
    kw = 'tillamook'
    output = fetch(kw)
    # store the results in JSON file
    with open('solution_1.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(output))
        print('Data successfully saved in solution_1.json')
