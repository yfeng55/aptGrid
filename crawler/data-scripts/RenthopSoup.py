import sys
import json
import csv
import time
import os.path
import urllib2
from bs4 import BeautifulSoup

request_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
request = urllib2.Request('https://www.renthop.com/search/nyc?page=0', headers=request_headers)

response = urllib2.urlopen(request)
content = response.read()

content = BeautifulSoup(content, "html.parser")

href_links = []

for links in content.findAll("a", {"class":"listing-title-link"}):
    href_links.append(links['href'])

for link in href_links:
    request = urllib2.Request(link, headers=request_headers)
    current_page = BeautifulSoup(urllib2.urlopen(request).read(), "html.parser")
    # print(current_page)
    all_photos = current_page.findAll("div", {"class":"fotorama"})[0].children
    photos_count = 0
    for photo in all_photos:
        photos_count += 1


#################################################################################

output = {}
output['num_photos'] = photos_count




"""
title = content.find("span", {"id":"titletextonly"}).text
neighborhood = content.find("span", {"class": "postingtitletext"}).find("small").text
available_date = content.find("span", {"class":"property_date"})['data-date']
price = content.find("span", {"class":"price"}).text;
num_beds = None;
num_baths = None;
square_ft = None;
listed_by = None;



# extract attributes from attrgroup
num_i = 0;
for child in content.find ("p", {"class":"attrgroup"}).findChildren():
	# print "\nchild " + str(num_i)
	# print child

	if(num_i == 1):
		num_beds = child.text
	elif(num_i == 2):
		num_baths = child.text
	elif(num_i == 4):
		square_ft = child.text
	elif(num_i == 7):
		listed_by = child.text
	num_i+=1




########################################################################

# create output object

output = {}

output['title'] = title
output['neighborhood'] = neighborhood
output['available_date'] = available_date
output['num_beds'] = num_beds
output['num_baths'] = num_baths
output['square_ft'] = square_ft
output['listed_by'] = listed_by
output['price'] = price


print json.dumps(output);
"""

"""
"title": "Example Listing 1",
		"lat": 111.111,
		"lng": 111.111,
		"neighborhood": "LES",
		"date": "06-24-2016",
		"description": "an example apartment listing (Lower East Side)",
		"contact_email": "contact@example.com",
		"contact_phone": "111-111-1111",
		"price": 4500,
		"bedrooms": 3,
		"bathrooms": 2,
		"has_livingroom": true,
		"has_kitchen": true,
		"allows_pets": false,
		"score": 9.3
"""