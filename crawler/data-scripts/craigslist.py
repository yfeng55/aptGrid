import time
import urllib2
import re
import utility
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver

driver = None
inner_driver = None

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def main():
    driver = webdriver.Chrome()
    inner_driver = webdriver.Chrome()
    db = utility.get_db()
    listings = []
    for min_rent in range(1000, 2000, 500):
        for page in range(0, 200, 100):
            url = "https://newyork.craigslist.org/search/aap?s=" + str(page) + "&max_price=" + str(
                min_rent + 500) + "&min_price=" + str(min_rent)
            request = urllib2.Request(url, headers=request_headers)
            response = urllib2.urlopen(request)
            content = BeautifulSoup(response.read(), "html.parser")
            output = create_new_listings(content, driver, inner_driver)

            listings.append(output)
            print(output, "\n")
            # db.listings.insert(output)

    driver.close()
    inner_driver.close()
    db.logout()


    # get neighborhood names
    for listing in listings:
        if listing["longitude"] != 0 and listing["latitude"] != 0:
            print "resolving neighborhood..."
            neighborhood = utility.find_neighborhood(float(listing["longitude"]), float(listing["latitude"]))
            listing["neighborhood"] = neighborhood

    return listings

def create_new_listings(content, driver, inner_driver):
    for links in content.findAll("a", {"class": "hdrlnk"}):
        # Catch all the exceptions because we do not want to stop execution.
        try:
            request_url = "https://newyork.craigslist.org" + links['href']

            driver.get(request_url)
            time.sleep(5)
            content = BeautifulSoup(driver.page_source, "html.parser")
            title = content.find("span", {"id": "titletextonly"}).text.encode('utf-8').strip()
            available_date = content.find("span", {"class": "property_date"})['data-date']
            price = content.find("span", {"class": "price"}).text

            # extract attributes from attrgroup
            num_i = 0
            for child in content.find("p", {"class": "attrgroup"}).findChildren():

                if num_i == 1:
                    try:
                        num_beds = int(child.text)
                    except ValueError:
                        num_beds = re.findall(r'\d+', child.text)[0]
                        # num_beds = [int(s) for s in child.text.split() if s.isdigit()][0]
                elif num_i == 2:
                    try:
                        num_baths = int(child.text)
                    except ValueError:
                        num_baths = re.findall(r'\d+', child.text)[0]
                        # num_baths = [int(s) for s in child.text.split() if s.isdigit()][0]
                elif num_i == 4:
                    try:
                        square_ft = float(child.text)
                    except ValueError:
                        square_ft = 0
                        print('Value error for sq ft in text ', child.text)
                elif num_i == 7:
                    listed_by = child.text.encode('utf-8').strip()
                num_i += 1

            lat_long = content.find("a", {"target": "_blank"})
            if lat_long is not None:
                parsed = re.search('(.*)@(.*)z(.*)', lat_long['href'])
                if parsed is not None:
                    latitude = float(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[0])
                    longitude = float(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[1])
                else:
                    inner_driver.get(lat_long['href'])
                    time.sleep(5)
                    new_lat_long = inner_driver.current_url.split('@')[1].split(',')
                    latitude = float(new_lat_long[0])
                    longitude = float(new_lat_long[1])
            else:
                latitude = 0.0
                longitude = 0.0
            description = content.find("section", {"id": "postingbody"}).text.encode('utf-8').strip()
            photo_wrapper = content.find("span", {"class": "slider-info"})
            if photo_wrapper is not None:
                num_photos = int(photo_wrapper.text.strip().split(" ")[3])
            else:
                num_photos = 0

            neighborhood = utility.find_neighborhood(longitude, latitude)

            output = {'title': title, 'neighborhood': neighborhood, 'available_date': available_date,
                      'num_beds': num_beds, 'num_baths': num_baths, 'square_ft': square_ft,
                      'listed_by': listed_by, 'price': price, 'latitude': latitude,
                      'longitude': longitude, 'link': driver.current_url, 'description': description,
                      'num_photos': num_photos}

            time.sleep(1)
            return output

        except:
            print("Unexpected error ", traceback.print_exc())
