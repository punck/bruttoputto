from sources.PuttoScraper import PuttoScraper
from sources.PuttoScraper import ChromeDriver


if __name__ == "__main__":    
    scraper = PuttoScraper(
        ChromeDriver().driver
    )
    scraper.get_content("https://bet.szerencsejatek.hu/jatekok/putto/sorsolasok")
    table = scraper.table
    scraper.finish()