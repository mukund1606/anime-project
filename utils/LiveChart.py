from bs4 import BeautifulSoup
import requests

import time

class LiveChart:
    BASE_URL = "https://www.livechart.me/"
    TIMETABLE_URL = "https://www.livechart.me/timetable"
    ANIME_URL = "https://www.livechart.me/anime/"  # + animeId
    SCHEDULE_URL = "https://www.livechart.me/schedule/all"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0"
        self.session.cookies.set("schedule_layout", "full")
        self.session.cookies.set(
            "preferences",
            "%7B%22sortby%22%3A%22airdate%22%2C%22time_zone%22%3A%22Etc%2FUTC%22%2C%22titles%22%3A%22romaji%22%2C%22ongoing%22%3A%22all%22%2C%22schedule_start%22%3A%22today%22%2C%22use_24h_clock%22%3Atrue%2C%22night_mode%22%3Atrue%2C%22reveal_spoilers%22%3Atrue%7D",
        )
        self.session.cookies.set("default_season", "nearest")

    # def timetable(self):
    #     page = self.session.get(self.TIMETABLE_URL)
    #     if page.status_code != 200:
    #         raise Exception("LiveChart is down")
    #     timetable_page = page.text
    #     soup = BeautifulSoup(timetable_page, "html.parser")
    #     date_wise_anime = {}
    #     container = soup.find("div", class_="timetable")
    #     days = container.find_all(
    #         "div", class_="timetable-day", attrs={"data-controller": "timetable-day"}
    #     )
    #     for day_div in days:
    #         anime_list = []
    #         date_timestamp = day_div.attrs.get("data-timetable-day-start")
    #         date = time.strftime("%d %B %Y", time.gmtime(int(date_timestamp)))
    #         divs = day_div.find_all(
    #             "div", class_="timetable-timeslot", attrs={"data-timestamp": True}
    #         )
    #         for animes_div in divs:
    #             timestamp = animes_div["data-timestamp"]
    #             all_animes = animes_div.find_all("div", class_="timetable-anime-block")
    #             for anime in all_animes:
    #                 anime_name = anime.find("a", class_="title")["title"]
    #                 anime_id = anime.find("a", class_="title")["href"].split("/")[-1]
    #                 episode = anime.find("div", class_="footer").text.split()
    #                 anime_list.append(
    #                     {
    #                         "name": anime_name,
    #                         "id": anime_id,
    #                         "episode": episode[0],
    #                         "premiere_time": timestamp,
    #                     }
    #                 )
    #             date_wise_anime[date] = anime_list
    #     return date_wise_anime

    def anime_data(self, anime_id):
        anime_info = {}
        page = self.session.get(self.ANIME_URL + anime_id)
        if page.status_code != 200:
            raise Exception("LiveChart is down")
        # Parse the HTML content of the page using BeautifulSoup
        page = page.text
        soup = BeautifulSoup(page, "html.parser")

        container_div = soup.find(
            "div", class_="flex mx-auto my-4 px-4 w-full max-w-5xl gap-x-6"
        )

        # Extract posters
        posters_element = container_div.find("div", class_="shrink-0")
        posters = (
            [
                src.strip().split(" ")[0]
                for src in posters_element.find("img").get("srcset").split(",")
            ]
            if posters_element
            else []
        )
        anime_info["posters"] = posters

        # Extract rating
        rating_element = container_div.find("span", class_="text-lg font-medium")
        max_rating = rating_element.find_next("span").text if rating_element else ""
        rating = rating_element.get_text() if rating_element else ""
        anime_info["rating"] = f"{rating}{max_rating}"

        # Extract titles
        titles = {
            "romaji": container_div.get("data-anime-details-romaji-title", ""),
            "english": container_div.get("data-anime-details-english-title", ""),
        }
        anime_info["titles"] = titles

        # Extract premiere date
        premiere_element = container_div.find("div", text="Premiere").find_next("a")
        premiere = premiere_element.text if premiere_element else ""
        anime_info["premiere"] = premiere

        # Extract season
        season_element = container_div.find("div", text="Season").find_next("a")
        season = season_element.text if season_element else ""
        anime_info["season"] = season

        # Extract official website
        website_element = container_div.find(
            "a", class_="lc-btn lc-btn-sm lc-btn-outline", href=True
        )
        website = website_element.get("href") if website_element else ""
        anime_info["website"] = website

        # Extract status
        status_element = container_div.find("div", text="Status")
        status = status_element.find_next("div").text if status_element else ""
        anime_info["status"] = status

        # Extract Original Title
        original_title_element = container_div.find("div", text="Original title")
        original_title = (
            original_title_element.fetchParents()[0]
            .text.replace("Original title", "")
            .strip()
            if original_title_element
            else ""
        )
        anime_info["titles"].update({"original": original_title})

        # Locate the desired HTML element with the class "card bg-base-300 shadow-md p-4 mt-4"
        anime_data_section = soup.find(
            "div", class_="card bg-base-300 shadow-md p-4 mt-4"
        )
        if anime_data_section:
            # Extract individual data points within the section
            anime_format = anime_data_section.find("div", text="Format")
            source = anime_data_section.find("div", text="Source")
            episodes_section = anime_data_section.find("div", text="Episodes")
            run_time_section = anime_data_section.find("div", text="Run time")

            # Check if "Format" section exists before extracting
            if anime_format:
                anime_format = anime_format.find_next("div").text
            else:
                anime_format = ""

            # Check if "Source" section exists before extracting
            if source:
                source = source.find_next("div").text
            else:
                source = ""

            # Check if "Episodes" section exists before extracting
            if episodes_section:
                episodes = episodes_section.find_next("div").text.split("/")[-1].strip()
            else:
                episodes = ""

            # Check if "Run time" section exists before extracting
            if run_time_section:
                run_time = (
                    run_time_section.fetchParents()[0]
                    .text.replace("Run time", "")
                    .strip()
                )
            else:
                run_time = ""

            description = soup.find(
                "div", {"data-expander-target": "content"}
            ).text.strip()
            studio_elements = soup.find("div", text="Studio")

            # Check if "Studio" section exists before extracting
            if studio_elements:
                studio_elements = studio_elements.find_next("div").find_all("a")
                studios = [studio.text for studio in studio_elements]
            else:
                studios = []

            # Extract tags
            tags_elements = soup.find("div", text="Tags")

            if tags_elements:
                tags_elements = tags_elements.find_next("div").find_all("a")
                tags = [tag.text for tag in tags_elements]
            else:
                tags = []

            anime_data = {
                "anime_format": anime_format,
                "source": source,
                "episodes": episodes,
                "run_time": run_time,
                "description": description,
                "studios": studios,
                "tags": tags,
            }
            anime_info.update(anime_data)

        # Extract IDs from external links
        external_links = container_div.find(
            "div", class_="grid grid-cols-2 md:grid-cols-3 gap-2"
        )
        ids = {}

        # Check if each external link element exists before extracting data
        anilist_link = container_div.find("a", class_="lc-btn-anilist")
        if anilist_link:
            ids["anilist_id"] = anilist_link["href"].split("/")[-1]
        else:
            ids["anilist_id"] = ""

        mal_link = container_div.find("a", class_="lc-btn-myanimelist")
        if mal_link:
            ids["mal_id"] = mal_link["href"].split("/")[-1]
        else:
            ids["mal_id"] = ""

        anidb_link = container_div.find("a", class_="lc-btn-anidb")
        if anidb_link:
            ids["anidb_id"] = anidb_link["href"].split("/")[-1]
        else:
            ids["anidb_id"] = ""

        animeplanet_link = container_div.find("a", class_="lc-btn-animeplanet")
        if animeplanet_link:
            ids["anime-planet_id"] = animeplanet_link["href"].split("/")[-1]
        else:
            ids["anime-planet_id"] = ""

        anisearch_link = container_div.find("a", class_="lc-btn-anisearch")
        if anisearch_link:
            ids["anisearch_id"] = anisearch_link["href"].split("/")[-1]
        else:
            ids["anisearch_id"] = ""

        kitsu_link = container_div.find("a", class_="lc-btn-kitsu")
        if kitsu_link:
            ids["kitsu_id"] = kitsu_link["href"].split("/")[-1]
        else:
            ids["kitsu_id"] = ""

        anime_info.update(ids)

        return anime_info

    def schedule(self):
        page = self.session.get(self.SCHEDULE_URL)
        if page.status_code != 200:
            raise Exception("LiveChart is down")
        schedule_page = page.text
        soup = BeautifulSoup(schedule_page, "html.parser")
        schedule_div = soup.find("div", class_="container")
        # Initialize a dictionary to store the schedule data
        schedule_data = {}

        # Find all the date headings
        all_dates = schedule_div.find_all("h4", class_="schedule-heading")

        # Loop through the date headings
        for elem in all_dates:
            articles_data = []
            data_div = elem.find_next(
                "div", attrs={"data-controller": "anime-card-list"}
            )

            # Find all anime articles within the date
            articles = data_div.find_all("article", class_="anime")

            # Loop through each anime article
            for anime_container in articles:
                anime_data = {}
                anime_data["livechart_id"] = anime_container.get("data-anime-id")
                anime_data["romaji_title"] = anime_container.get("data-romaji")
                anime_data["english_title"] = anime_container.get(
                    "data-english"
                )  # Fixed attribute name
                anime_data["native_title"] = anime_container.get("data-native")
                anime_data["alternate_titles"] = eval(
                    anime_container.get("data-alternate")
                )
                anime_data["premiere_timestamp"] = int(
                    anime_container.get("data-premiere")
                )
                anime_data["main_title"] = anime_container.find(
                    "a", {"data-anime-card-target": "mainTitle"}
                ).text
                anime_data["genres"] = [
                    a.text for a in anime_container.select(".anime-tags a")
                ]
                anime_data["studio"] = [
                    studio.text for studio in anime_container.select(".anime-studios a")
                ]
                anime_data["premiere_date"] = anime_container.select_one(
                    ".anime-date"
                ).text
                anime_data["synopsis"] = anime_container.select_one(
                    ".anime-synopsis"
                ).text.strip()
                anime_data["anime_source"] = anime_container.select_one(
                    ".anime-source"
                ).text  # Fixed attribute name
                anime_data["anime_episodes"] = anime_container.select_one(
                    ".anime-episodes"
                ).text

                # Extract related links
                related_links = anime_container.select(".related-links a")
                for link in related_links:
                    class_name = link.get("class")[0].replace("-icon", "")
                    link_url = link.get("href")
                    class_list = [
                        "anilist",
                        "mal",
                        "anidb",
                        "anime-planet",
                        "anisearch",
                        "kitsu",
                        "website"
                    ]
                    # Check and store specific link types
                    for elem_class in class_list:
                        if class_name in class_list:
                            if class_name != "website":
                                anime_data[class_name + "_id"] = link_url.split("/")[-1]
                            else:
                                anime_data[class_name] = link_url
                        else:
                            anime_data[class_name + "_id"] = None

                # Extract poster images
                poster_div = anime_container.find("div", class_="poster-container")
                image = poster_div.find("img")
                image_attrs = image.attrs
                anime_data["posters"] = [
                    src.strip().split(" ")[0]
                    for src in image_attrs.get("srcset").split(",")
                ]

                articles_data.append(anime_data)

            schedule_data[elem.text] = articles_data
        return schedule_data
