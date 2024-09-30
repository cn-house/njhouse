# coding:utf-8

import re
from typing import Optional

from bs4 import BeautifulSoup
from sitepages import page


class njhouse_page():
    def __init__(self, url: str):
        self.__page: page = page(url=url)
        self.__cache: Optional[str] = None
        self.__soup: Optional[BeautifulSoup] = None

    @property
    def page(self) -> page:
        return self.__page

    @property
    def cache(self) -> str:
        if self.__cache is None:
            self.__cache = self.fetch()
        return self.__cache

    def fetch(self) -> str:
        return self.page.fetch()


class njhouse_soup(njhouse_page):
    def __init__(self, url: str):
        self.__soup: Optional[BeautifulSoup] = None
        super().__init__(url=url)

    @property
    def soup(self) -> BeautifulSoup:
        if self.__soup is None:
            self.__soup = BeautifulSoup(self.cache, "html.parser")
        return self.__soup


class njhouse_project(njhouse_soup):
    def __init__(self, url: str = "https://www.njhouse.com.cn/projectindex.html"):  # noqa:E501
        super().__init__(url=url)

    @property
    def subscriptions(self) -> int:
        """认购套数
        """
        match = self.soup.find("div", class_="busniess_num_word")
        return int(match.get_text(strip=True)) if match else 0

    @property
    def transactions(self) -> int:
        """成交套数
        """
        match = self.soup.find("div", class_="busniess_num_word green")
        return int(match.get_text(strip=True)) if match else 0

    @property
    def sales(self) -> int:
        """销售 = 认购 + 成交
        """
        return self.subscriptions + self.transactions


class njhouse_stock(njhouse_page):
    def __init__(self, url: str = "http://njzl.njhouse.com.cn/stock"):
        super().__init__(url=url)

    @property
    def total_listings(self) -> int:
        """总挂牌房源
        """
        match = re.search(r"(总挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def intermediary_listings(self) -> int:
        """中介挂牌房源
        """
        match = re.search(r"(中介挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def personal_listings(self) -> int:
        """个人挂牌房源
        """
        match = re.search(r"(个人挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def yesterday_tradings(self) -> int:
        """昨日住宅成交量
        """
        match = re.search(r"(昨日住宅成交量：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0


class njhouse_rent(njhouse_page):
    def __init__(self, url: str = "http://njzl.njhouse.com.cn/rent"):
        super().__init__(url=url)

    @property
    def listings(self) -> int:
        """挂牌量
        """
        match = re.search(r"(挂牌量：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0
