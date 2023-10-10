from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

# Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

import time
import datetime

from utils.browser import Browser


class LiveChart:
    BASE_URL = "https://www.livechart.me/"
    TIMETABLE_URL = "https://www.livechart.me/timetable"

    def __init__(self) -> None:
        self.date = None
        self.timetablePage = None
        self.borwser = Browser()

    def timetable(self) -> list | None:
        date = time.strftime(
            "%Y-%m-%d",
            time.gmtime(
                datetime.datetime.now(datetime.timezone.utc)
                .replace(tzinfo=datetime.timezone.utc)
                .timestamp()
            ),
        )
        if self.date == None or self.date != date or self.timetablePage == None:
            self.wait = WebDriverWait(self.borwser.driver, 100)
            self.borwser.driver.get(
                self.TIMETABLE_URL + "?time_zone=UTC" + "&date=" + date
            )
            self.borwser.driver.implicitly_wait(100)
            self.timetablePage = self.borwser.driver.page_source
            self.date = date
        soup = BeautifulSoup(self.timetablePage, "html.parser")
        animeList = []
        date_wise_anime = {}
        divs = soup.find_all(
            "div", class_="timetable-timeslot", attrs={"data-timestamp": True}
        )
        for animes_div in divs:
            timestamp = animes_div["data-timestamp"]
            animeTime = time.strftime("%H:%M", time.gmtime(int(timestamp)))
            animeDay = time.strftime("%A", time.gmtime(int(timestamp)))
            date = time.strftime("%d %B %Y", time.gmtime(int(timestamp)))
            for anime in animes_div.find_all("div", class_="timetable-anime-block"):
                animeName = anime.find("a", class_="title")["title"]
                animeId = anime.find("a", class_="title")["href"].split("/")[-1]
                episode = anime.find("div", class_="footer").text.split()
                animeList.append(
                    {
                        "name": animeName,
                        "id": animeId,
                        "episode": episode[0],
                        "dateData": {
                            "date": date,
                            "time": animeTime,
                            "day": animeDay,
                        },
                    }
                )
        for anime in animeList:
            if anime["dateData"]["date"] not in date_wise_anime:
                date_wise_anime[anime["dateData"]["date"]] = []
            date_wise_anime[anime["dateData"]["date"]].append(anime)
        return date_wise_anime
