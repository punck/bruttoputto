from sources.driver import ChromeDriver
from sources.scraper import PuttoScraper


if __name__ == "__main__":    
    scraper = PuttoScraper(
        ChromeDriver().driver
    )
    scraper.get_content("https://bet.szerencsejatek.hu/jatekok/putto/sorsolasok")
    table = scraper.table
    scraper.finish()