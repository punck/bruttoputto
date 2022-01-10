import requests
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup


class PuttoScraper:
    CSRF = "065ef323b39f19661814eab6034ea76bbe194bb0"
    
    def __init__(self):
        self._url = "https://bet.szerencsejatek.hu/jatekok/putto/sorsolasok/#"
        
    def get_table(self, date: str = None):     
        response = requests.post(
            self._url,
            headers=self._get_headers(),
            data=self._get_payload(date),
            files=None
        )
        
        if response.status_code == 200:
            return self._parse_table(response.text)
      
    def _get_payload(self, date: str):
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
        else:
            date = datetime.today()
            
        year, week, day = datetime.date(date).isocalendar()
        
        return {
            "year": year,
            "week": week,
            "day": day,
            "CSRF_9cd258d5": self.CSRF
        }
    
    def _get_headers(self):
        return {
            "Cookie": f"CSRF_9cd258d5={self.CSRF}"
        }
        
                        
    def _parse_table(self, html):
        res = []
        soup = BeautifulSoup(html, "html.parser")
        table_div = soup.find("div", {"class": "table-container clear"})
        table = table_div.find("table")
        tbody = table.find("tbody")
        
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            res.append([ele for ele in cols if ele])
        
        return res
