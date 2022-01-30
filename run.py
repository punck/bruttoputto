from sources.scraper import PuttoScraper

if __name__ == "__main__":
    scraper = PuttoScraper()

    # date format: YYYY-MM-DD
    # res = scraper.fetch_table("1913-05-23")

    #scraper.fetch_all()
    res = scraper.result
    #scraper.dump_binary()
    #scraper.dump_text()

    print(len(res))
