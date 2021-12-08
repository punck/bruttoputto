from selenium.webdriver.common.by import By


class PuttoScraper:
    def __init__(self, driver):
        self._driver = driver
        self._table = []
        
    def get_content(self, url):
        self._driver.get(url)
        
    def finish(self):
        self._driver.quit()
        
    def _fill_table(self):
        table_container = self._driver.find_element(
            By.CLASS_NAME,
            "table-container"
        )
        table = table_container.find_element(
            By.TAG_NAME,
            "table"
        )
        
        for row in table.find_elements(By.TAG_NAME, "tr"):
            cols = row.find_elements(By.TAG_NAME, "td")
            
            if cols:
                self._table.append(
                    f"{cols[0].text};{cols[1].text};{cols[2].text};{cols[3].text}"
                )
    
    @property
    def table(self):
        self._fill_table()
        return self._table
        
    