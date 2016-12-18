import time
import urllib2
import re
from bs4 import BeautifulSoup
import traceback
import utility
from selenium import webdriver

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
page_limit = 10
driver = webdriver.Chrome()

# Static strings for finding values in the html tags

link_finder = {"class": "listing-title-link"}
contact_name_finder = {"class": "font-size-90 color-fg-blue"}
title_finder = {
    "style": "font-size: 1.45em; width: 400px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;"}
neighborhood_finder = {
    "style": "font-size: 0.95em; margin-top: 4px; color: #666666; width: 400px; white-space: nowrap; text-overflow: "
             "ellipsis; overflow: hidden;"}
beds_baths_finder = {"style": "font-weight: bold; color: #444444;"}
price_finder = {"style": "font-size: 1.45em; color: #005826; text-align: right;"}
description_finder = {"style": "font-size: 0.90em; line-height: 140%;"}
photo_finder = {"class": "fotorama"}
available_date_finder = {
    "style": "font-size: 0.95em; color: #666666; padding-left: 10px; border-left: 1px solid #eeeeee;"}
lat_long_finder = {"title": "Click to see this area on Google Maps"}


# Create the new listing from the current page and return its
def create_new_listing(current_page, link):
    try:
        all_photos = current_page.findAll("div", photo_finder)[0].children
        photos_count = 0
        for _ in all_photos:
            photos_count += 1

        contact_name = current_page.find("a", contact_name_finder).text.encode('utf-8').strip()
        title = current_page.find("div", title_finder).text.strip()

        beds_baths = current_page.findAll("span", beds_baths_finder)
        # STUDIO = 0 num_beds
        try:
            num_beds = int(beds_baths[0].text.strip())
        except ValueError:
            num_beds = 0
        num_baths = int(beds_baths[1].text.strip())

        price = float(current_page.find("div", price_finder).text.replace("$", "").replace(",", ".").strip())
        description = current_page.find("div", description_finder).encode('utf-8').strip()
        # Available date can be either Immediate or MM-DD-YYYY
        available_date = current_page.find("td", available_date_finder).text.strip()
        lat_long = current_page.find("a", lat_long_finder)['href']

        parsed = re.search('(.*)ll=(.*)z=(.*)', lat_long)
        latitude = float(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[0])
        longitude = float(parsed.group(2)[:len(parsed.group(2)) - 2].split(',')[1])

        neighborhood = utility.find_neighborhood(longitude, latitude)
        # craigslist has square foot info available but renthop does not
        listing = {'title': title, 'neighborhood': neighborhood, 'available_date': available_date,
                   'num_beds': num_beds, 'num_baths': num_baths, 'square_ft': 0, 'price': price,
                   'description': description, 'num_photos': photos_count, 'listed_by': contact_name,
                   'link': link['href'].strip().encode('utf-8').strip(), 'latitude': latitude, 'longitude': longitude}
        # listing['link'] = str(link['href'].strip())
        # print json.dumps(listing)
        return listing
    except ValueError:
        print("Value error ", traceback.print_exc())
    except:
        print("Unexpected error ", traceback.print_exc())


# Get page_limit number of pages from renthop and pass them on to get parsed

def main():
    listings = []
    for i in range(0, page_limit):
        request = urllib2.Request('https://www.renthop.com/search/nyc?page=' + str(i), headers=request_headers)
        response = urllib2.urlopen(request)
        content = BeautifulSoup(response.read(), "html.parser")
        for link in content.findAll("a", link_finder):
            driver.get(link['href'])
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            listing = create_new_listing(soup, link)
            listings.append(listing)

    driver.close()
    return listings
