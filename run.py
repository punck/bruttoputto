from sources.scraper import PuttoScraper

if __name__ == "__main__":    
    scraper = PuttoScraper()
    
    # date format: YYYY-MM-DD
    res = scraper.get_table("2022-01-11")