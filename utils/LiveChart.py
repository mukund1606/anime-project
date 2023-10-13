from bs4 import BeautifulSoup
import requests

import time


class LiveChart:
    BASE_URL = "https://www.livechart.me/"
    TIMETABLE_URL = "https://www.livechart.me/timetable"
    ANIME_URL = "https://www.livechart.me/anime/"  # + animeId
    SCHEDULE_URL = "https://www.livechart.me/schedule/all"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0"
        self.session.cookies.set("schedule_layout", "full")
        self.session.cookies.set(
            "preferences",
            "%7B%22sortby%22%3A%22airdate%22%2C%22time_zone%22%3A%22Etc%2FUTC%22%2C%22titles%22%3A%22romaji%22%2C%22ongoing%22%3A%22all%22%2C%22schedule_start%22%3A%22today%22%2C%22use_24h_clock%22%3Atrue%2C%22night_mode%22%3Atrue%2C%22reveal_spoilers%22%3Atrue%7D",
        )
        self.session.cookies.set("default_season", "nearest")

    def timetable(self) -> list:
        page = self.session.get(self.TIMETABLE_URL)
        if page.status_code != 200:
            raise Exception("LiveChart is down")
        timetable_page = page.text
        soup = BeautifulSoup(timetable_page, "html.parser")
        date_wise_anime = {}
        container = soup.find("div", class_="timetable")
        days = container.find_all(
            "div", class_="timetable-day", attrs={"data-controller": "timetable-day"}
        )
        for day_div in days:
            anime_list = []
            date_timestamp = day_div.attrs.get("data-timetable-day-start")
            date = time.strftime("%d %B %Y", time.gmtime(int(date_timestamp)))
            divs = day_div.find_all(
                "div", class_="timetable-timeslot", attrs={"data-timestamp": True}
            )
            for animes_div in divs:
                timestamp = animes_div["data-timestamp"]
                all_animes = animes_div.find_all("div", class_="timetable-anime-block")
                for anime in all_animes:
                    anime_name = anime.find("a", class_="title")["title"]
                    anime_id = anime.find("a", class_="title")["href"].split("/")[-1]
                    episode = anime.find("div", class_="footer").text.split()
                    anime_list.append(
                        {
                            "name": anime_name,
                            "id": anime_id,
                            "episode": episode[0],
                            "premiere_time": timestamp,
                        }
                    )
                date_wise_anime[date] = anime_list
        return date_wise_anime

    def anime_data(self, anime_id) -> list:
        page = self.session.get(self.ANIME_URL + anime_id)
        if page.status_code != 200:
            raise Exception("LiveChart is down")
        page = page.text
        studio = None
        soup = BeautifulSoup(page, "html.parser")
        container_div = soup.find_all("div", class_="grow w-0")[0]
        title_div = container_div("div", class_="grow")[0]
        titles = title_div.find_all("span", class_="text-base-content")
        title = titles[0].text
        english_title = titles[1].text
        info_div = container_div.find("div", class_="card")
        sub_divs = info_div.find_all("div")
        description = info_div.find(
            "div", attrs={"data-expander-target": "content"}
        ).text
        tags_div = sub_divs[-1]
        tags = [tag.text for tag in tags_div.find_all("a")]
        if sub_divs[-4].text == "Studio":
            studio_div = sub_divs[-3]
            studio = [s.text for s in studio_div.find_all("a")]
        return {
            "title": title,
            "english_title": english_title,
            "description": description,
            "studios": studio,
            "tags": tags,
        }

    def schedule(self) -> list:
        page = self.session.get(self.SCHEDULE_URL)
        if page.status_code != 200:
            raise Exception("LiveChart is down")
        schedule_page = page.text
        soup = BeautifulSoup(schedule_page, "html.parser")
        schedule_div = soup.find("div", class_="container")
        all_dates = schedule_div.find_all("h4", class_="schedule-heading")
        schedule_data = {}
        for elem in all_dates:
            articles_data = []
            data_div = elem.find_next(
                "div", attrs={"data-controller": "anime-card-list"}
            )
            articles = data_div.find_all("article", class_="anime")
            for article in articles:
                anime_data = {}
                attributes = article.attrs
                anime_data["id"] = attributes.get("data-anime-id")
                anime_data["title"] = attributes.get("data-romaji")
                anime_data["english_title"] = attributes.get("data-english")
                anime_data["native_title"] = attributes.get("data-native")
                anime_data["alternative_titles"] = attributes.get("data-alternate")
                anime_data["premiere_time"] = attributes.get("data-premiere")
                tags_div = article.find("ol", class_="anime-tags")
                anime_data["tags"] = [tag.text for tag in tags_div.find_all("a")]
                poster_div = article.find("div", class_="poster-container")
                image = poster_div.find("img")
                image_attrs = image.attrs
                anime_data["posters"] = [
                    src.strip().split(" ")[0]
                    for src in image_attrs.get("srcset").split(",")
                ]
                articles_data.append(anime_data)
            schedule_data[elem.text] = articles_data
        return schedule_data
