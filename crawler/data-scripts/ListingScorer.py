import json
from pymongo import MongoClient
import math

# with open('sample_formatted.json') as data_file:
#    listings = json.loads(data_file.read())

# with open('test.json') as data_file:
#    test_listings = json.loads(data_file.read())

MIN_PRICE = 200
SCAM_POSTERS = []


def getSpamScore(listing, zscore):
    if listing["price"]<MIN_PRICE:
        return 0
    elif listing["listed_by"] in SCAM_POSTERS:
        return 0
    else:
        return max(0, (2.5*math.log(listing["num_photos"]+1)/1.39794000867)+(4.5*math.log(zscore+7)) +
                   (len(listing["description"])/500))


def get_db():
    connection = MongoClient('ds023654.mlab.com', 23654)
    db = connection['apartmentdb']
    db.authenticate('admin', 'craigslistsucks')
    return db


def main(listings, test_listings):
    # -------------------finding avg data for each neighborhood--------------------------------
    total_prices = {}
    counts = {}
    avg_price = {}
    std_numerator = {}
    std_deviataion = {}
    db = get_db()
    dbtotal = {}

    for listing in listings:
        key = listing["neighborhood"]+'_'+str(listing["num_beds"])
        if key in total_prices:
            total_prices[key] += listing["price"]
            counts[key] += 1
        else:
            total_prices[key] = listing["price"]
            counts[key] = 1

    print total_prices
        
    for key in total_prices:
        temp_listing = db.neighborhoods.find_one({'name': key})
        print(key)
        dbtotal[key] = temp_listing['avg_price']*temp_listing['count']

        avg_price[key] = (total_prices[key]+dbtotal[key])/float((counts[key]+temp_listing["count"]))
        db.neighborhoods.update_one({
            '_id': temp_listing["_id"]
            }, {
              '$set': {
                "avg_price": avg_price[key],
                "count": temp_listing["count"] + counts[key]

              }
            }, upsert=False)

    # logging
    # print avgPrice

    for listing in listings:
        key = listing["neighborhood"]+"_"+str(listing["num_beds"])
        if key in std_numerator:
            std_numerator[key] += pow(listing["price"]-avg_price[key], 2)
        else:
            std_numerator[key] = pow(listing["price"]-avg_price[key], 2)

    for key in std_numerator:
        std_deviataion[key] = (std_numerator[key]/counts[key])**0.5

    # logging
    # print std_deviataion

    # ---------------------spam detection----------------------------------------------------------
    zscore = {}
    spam_score = {}

    for listing in test_listings:

        try:
            key = listing["neighborhood"]+"_"+str(listing["num_beds"])
            
            if key not in std_deviataion.keys():
                zscore[listing["link"]] = 0
                listing["zscore"] = 0
            elif std_deviataion[key] == 0:
                zscore[listing["link"]] = 0
                listing["zscore"] = 0
            else:
                zscore[listing["link"]] = (listing["price"]-avg_price[key])/std_deviataion[key]
                spam_score[listing["link"]] = getSpamScore(listing, zscore[listing["link"]])

                listing["zscore"] = (listing["price"]-avg_price[key])/std_deviataion[key]
                listing["spam_score"] = spam_score[listing["link"]]


            print "\ninserting..."
            print listing
            db.listings.insert(listing)
        except:
            print "\nunable to insert"
            print listing


    for listing in listings:
        db.listings.insert(listing)



