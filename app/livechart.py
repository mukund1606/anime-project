from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

# Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

import time


class LiveChart:
    BASE_URL = "https://www.livechart.me/"
    TIMETABLE_URL = "https://www.livechart.me/timetable"

    def __init__(self) -> None:
        self.home_page_data = None
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_service = ChromeService(ChromeDriverManager().install())
        self.available_browser = "chrome"
        self.driver = webdriver.Chrome(
            service=self.chrome_service, options=self.chrome_options
        )
        # self.driver = webdriver.Remote(
        #     "http://127.0.0.1:4444/wd/hub", options=self.chrome_options
        # )

    def scrape_home(self) -> list | None:
        try:
            if self.home_page_data is None:
                self.wait = WebDriverWait(self.driver, 100)
                self.driver.get(self.BASE_URL)
                self.driver.implicitly_wait(100)
                self.home_page_data = self.driver.page_source
            soup = BeautifulSoup(self.home_page_data, "html.parser")
            divs = soup.find_all("div", class_="anime-card")
            return divs
        except Exception as e:
            return None
        finally:
            self.driver.quit()

    def timetable(self) -> list | None:
        # try:
        if self.home_page_data is None:
            self.wait = WebDriverWait(self.driver, 100)
            self.driver.get(self.TIMETABLE_URL + "?time_zone=UTC")
            self.driver.implicitly_wait(100)
            self.home_page_data = self.driver.page_source
        soup = BeautifulSoup(self.home_page_data, "html.parser")
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
