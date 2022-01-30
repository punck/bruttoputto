import os
import pickle
from datetime import datetime, timedelta
from typing import Optional, Union, List, Dict

import requests
from bs4 import BeautifulSoup


class PuttoScraper:
    CSRF = "065ef323b39f19661814eab6034ea76bbe194bb0"

    DATA_DIRECTORY = "output"
    DATA_FILE_NAME = "bruttoputto"
    DATE_FORMAT = "%Y-%m-%d"

    MAX_EMPTY_DAYS = 5

    def __init__(self):
        self._url = "https://bet.szerencsejatek.hu/jatekok/putto/sorsolasok/#"
        self._result = []

        os.makedirs(self.DATA_DIRECTORY, exist_ok=True)

        self.load_binary()
        self._cntr = 0

    @property
    def result(self) -> List[List[str]]:
        return self._result

    def fetch_table(self, date: Optional[Union[str, datetime]]) -> List:
        response = requests.post(
            self._url,
            headers=self._get_headers(),
            data=self._get_payload(date),
            files=None
        )

        if response.status_code == 200:
            return self._parse_table(response.text)

    def fetch_latest(self):
        latest = self._get_latest_date()
        date = datetime.today()
        while date >= latest:
            self._result.extend(self.fetch_table(date))
            date = date - timedelta(days=1)

        self._result = [list(x) for x in set(tuple(x) for x in self._result)]
        self._result.sort(reverse=True)

        self.dump_binary()
        self.dump_text()

    def fetch_all(self):
        self._cntr = 0
        self._result = []
        date = datetime.today()
        table = self.fetch_table(date)
        self.dump_binary()
        self.dump_text()

        while table is not None and self._cntr < self.MAX_EMPTY_DAYS:
            if not table:
                self._cntr += 1
                print(f"No result for {self._cntr} consecutive days")
            else:
                self._cntr = 0

            print(f"Fetching {date.strftime(self.DATE_FORMAT)}")

            self._result.extend(table)
            date = date - timedelta(days=1)
            table = self.fetch_table(date)
            self.dump_binary()
            self.dump_text()

    def dump_binary(self):
        with open(f"{os.path.join(self.DATA_DIRECTORY, self.DATA_FILE_NAME)}.pkl", "wb") as f:
            pickle.dump(self._result, f)

    def dump_text(self):
        with open(f"{os.path.join(self.DATA_DIRECTORY, self.DATA_FILE_NAME)}.txt", "w") as f:
            for item in self._result:
                f.write(f"{item}\n")

    def load_binary(self):
        try:
            self._result = pickle.load(open(f"{os.path.join(self.DATA_DIRECTORY, self.DATA_FILE_NAME)}.pkl", "rb"))
        except FileNotFoundError as fnfe:
            print(f"{fnfe}")
            pass

    def _get_payload(self, date: Optional[Union[str, datetime]]) -> Dict:
        if type(date) == str:
            date = datetime.strptime(date, "%Y-%m-%d")
        date = date or datetime.today()

        year, week, day = datetime.date(date).isocalendar()

        return {
            "year": year,
            "week": week,
            "day": day,
            "CSRF_9cd258d5": self.CSRF
        }

    def _get_headers(self) -> Dict:
        return {
            "Cookie": f"CSRF_9cd258d5={self.CSRF}"
        }

    def _get_latest_date(self):
        return self._convert_datestring(max([row[0] for row in self._result]))

    @staticmethod
    def _convert_datestring(date: str):
        return datetime.strptime("{}-{}-{} {}".format(*date.split(". ")),  "%Y-%m-%d %H:%M")

    @staticmethod
    def _parse_table(html: str) -> List[List[str]]:
        res = []
        soup = BeautifulSoup(html, "html.parser")
        table_div = soup.find("div", {"class": "table-container clear"})

        if table_div:
            table = table_div.find("table")
            tbody = table.find("tbody")

            rows = tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                res.append([ele for ele in cols if ele])

            return res

        closed_div = soup.find("div", {"class": "box closed-game clear"})
        if closed_div:
            return []
