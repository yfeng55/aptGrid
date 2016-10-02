# produces a single apartment listing JSON file given a URL for the listing

# EXAMPLE:
# python fetch-single-page.py [listing url]

import sys
import json
import csv
import time
import os.path
import urllib2
from bs4 import BeautifulSoup


request_url = sys.argv[1];
# print "request URL: " + request_url


# download page as HTML file
# print("downloading... " + request_url + "\n")
request_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
request = urllib2.Request(request_url, headers=request_headers)

response = urllib2.urlopen(request)
content = response.read()


# extract data from HTML document 
content = BeautifulSoup(content, "html.parser")

# declare data fields
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

















