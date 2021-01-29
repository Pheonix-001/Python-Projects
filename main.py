import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    temp = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')

    # add term query to url
    url1 = temp.format(search_term)

    #add page query placeholder
    url1 += '&page{}'

    # return temp.format(search_term)
    return url1

def extract_record(item):

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return 

    try:
        # rank and rating
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)

    return result

def main(search_term):
    
    chromedriver = ".\chromedriver"
    driver = webdriver.Chrome(chromedriver)

    records = []
    url = get_url(search_term)

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})


        for i in results:
            record = extract_record(i)
            if record:
                records.append(record)

    driver.close()

    with open('iphones12.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount'])
        writer.writerows(records)


main('iphone 12')

