import json
import math

# with open('sample_formatted.json') as data_file:
#     listings = json.loads(data_file.read())

# with open('test.json') as data_file:
#     test_listings = json.loads(data_file.read())

MIN_PRICE = 200
SCAM_POSTERS = []


def get_spam_score(listing, zscore):
    if listing["price"] < MIN_PRICE:
        return 0
    elif listing["listed_by"] in SCAM_POSTERS:
        return 0
    else:
        return max(0, (2.5 * math.log(listing["num_photos"] + 1) / 1.39794000867) + (4.5 * math.log(zscore + 7)) +
                   (len(listing["description"]) / 500))


def main(listings, test_listings):
    # -------------------finding avg data for each neighborhood--------------------------------
    total_price = {}
    counts = {}
    avg_price = {}
    std_numerator = {}
    std_deviataion = {}

    for listing in listings:
        key = listing["neighborhood"] + str(listing["num_beds"])
        if key in total_price:
            total_price[key] += listing['price']
            counts[key] += 1
        else:
            total_price[key] = listing['price']
            counts[key] = 1

    for key in total_price:
        total_price[key] = total_price[key] / counts[key]

    # logging
    # print avg_price

    for listing in listings:
        key = listing["neighborhood"] + str(listing["num_beds"])
        if key in std_numerator:
            std_numerator[key] += pow(listing["price"] - avg_price[key], 2)
        else:
            std_numerator[key] = pow(listing["price"] - avg_price[key], 2)

    for key in std_numerator:
        std_deviataion[key] = (std_numerator[key] / counts[key]) ** 0.5

    # logging
    # print std_deviataion

    # ---------------------spam detection----------------------------------------------------------
    zscore = {}
    spam_score = {}

    for listing in test_listings:
        key = listing["neighborhood"] + str(listing["num_beds"])
        if std_deviataion[key] == 0:
            zscore[listing["link"]] = 0
        else:
            zscore[listing["link"]] = (listing["price"] - avg_price[key]) / std_deviataion[key]

            spam_score[listing["link"]] = get_spam_score(listing, zscore[listing["link"]])
        # print spam_score[listing["link"]]


# if __name__ == "__main__":
#     main()
