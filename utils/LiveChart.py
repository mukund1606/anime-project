from bs4 import BeautifulSoup
import requests

import time
import datetime


class LiveChart:
    BASE_URL = "https://www.livechart.me/"
    TIMETABLE_URL = "https://www.livechart.me/timetable"

    def __init__(self) -> None:
        self.date = None
        self.timetablePage = None
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0"

    def timetable(self) -> list:
        date = time.strftime(
            "%Y-%m-%d",
            time.gmtime(
                datetime.datetime.now(datetime.timezone.utc)
                .replace(tzinfo=datetime.timezone.utc)
                .timestamp()
            ),
        )
        if self.date == None or self.date != date or self.timetablePage == None:
            self.timetablePage = self.session.get(
                self.TIMETABLE_URL + "?time_zone=UTC" + "&date=" + date
            ).text
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
