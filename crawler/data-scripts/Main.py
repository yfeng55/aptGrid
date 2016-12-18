import RenthopSoup
import craigslist
import ListingScorer


def main():
    # listings = RenthopSoup.main()
    # print(listings)
    test_listings = craigslist.main()

    print "------ test listings -------"
    print test_listings[0]

    ListingScorer.main([], test_listings=test_listings)

if __name__ == "__main__":
    main()
