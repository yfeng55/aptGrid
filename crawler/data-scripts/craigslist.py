import json
import time
import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver


def get_db():
    connection = MongoClient('ds023654.mlab.com', 23654)
    db = connection['apartmentdb']
    db.authenticate('admin', 'craigslistsucks')
    return db


driver = webdriver.Chrome()

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def main():
    db = get_db()
    for min_rent in range(1000, 2000, 500):
        for page in range(0, 2500, 100):
            url = "https://newyork.craigslist.org/search/aap?s=" + str(page) + "&max_price=" + str(
                min_rent + 500) + "&min_price=" + str(min_rent)
            request = urllib2.Request(url, headers=request_headers)
            response = urllib2.urlopen(request)
            content = BeautifulSoup(response.read(), "html.parser")
            output = create_new_listings(content)
            db.listings.insert(output)

    driver.close()
    db.logout()


def create_new_listings(content):
    for links in content.findAll("a", {"class": "hdrlnk"}):
        request_url = "https://newyork.craigslist.org" + links['href']

        driver.get(request_url)
        time.sleep(5)
        content = BeautifulSoup(driver.page_source, "html.parser")

        try:
            title = content.find("span", {"id": "titletextonly"}).text
        except AttributeError:
            title = "None"

        try:
            neighborhood = content.find("span", {"class": "postingtitletext"}).find("small").text
        except AttributeError:
            neighborhood = "None"

        try:
            available_date = content.find("span", {"class": "property_date"})['data-date']
        except AttributeError:
            available_date = "None"

        try:
            price = content.find("span", {"class": "price"}).text
        except AttributeError:
            price = "None"

        num_beds = None
        num_baths = None
        square_ft = None
        listed_by = None

        # extract attributes from attrgroup
        num_i = 0
        for child in content.find("p", {"class": "attrgroup"}).findChildren():
            # print "\nchild " + str(num_i)
            # print child

            if num_i == 1:
                num_beds = child.text
            elif num_i == 2:
                num_baths = child.text
            elif num_i == 4:
                square_ft = child.text
            elif num_i == 7:
                listed_by = child.text
            num_i += 1

        latitude = 0
        longitude = 0
        lat_long = content.find("a", {"target": "_blank"})
        if lat_long is not None:
            print(lat_long['href'])
            parsed = re.search('(.*)@(.*)z(.*)', lat_long['href'])
            if parsed is not None:
                latitude = str(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[0])
                longitude = str(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[1])
            else:
                inner_driver = webdriver.Chrome()
                inner_driver.get(lat_long['href'])
                time.sleep(5)
                new_lat_long = inner_driver.current_url.split('@')[1].split(',')
                latitude = str(new_lat_long[0])
                longitude = str(new_lat_long[1])
                inner_driver.close()

        description = content.find("section", {"id": "postingbody"}).text.strip()
        photo_wrapper = content.find("span", {"class": "slider-info"})
        num_photos = 0
        if photo_wrapper is not None:
            num_photos = photo_wrapper.text.strip().split(" ")[3]

        output = {'title': str(title), 'neighborhood': str(neighborhood), 'available_date': str(available_date),
                  'num_beds': str(num_beds), 'num_baths': str(num_baths), 'square_ft': str(square_ft),
                  'listed_by': str(listed_by), 'price': str(price), 'latitude': str(latitude),
                  'longitude': str(longitude), 'link': str(driver.current_url), 'description': str(description),
                  'num_photos': str(num_photos)}

        print json.dumps(output)
        time.sleep(1)
        return output


if __name__ == "__main__":
    main()
