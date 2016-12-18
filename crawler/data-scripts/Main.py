import RenthopSoup
import craigslist
import ListingScorer


def main():
    listings = RenthopSoup.main()
    # print(listings)
    # test_listings = craigslist.main()
    ListingScorer.main(listings, test_listings=listings)

if __name__ == "__main__":
    main()
