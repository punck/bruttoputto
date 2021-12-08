from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from abc import abstractmethod


class Driver():
    def __init__(self):
        self._options = Options()
        self._options.add_argument("--headless")
        
    @property
    @abstractmethod
    def driver(self):
        pass


class ChromeDriver(Driver):        
    @property
    def driver(self):
        self._service = Service(
            ChromeDriverManager().install()
        )
        self._driver = webdriver.Chrome(
            service = self._service,
            options = self._options
        )
        
        return self._driver
    