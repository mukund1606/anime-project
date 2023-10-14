from pydantic import BaseModel
from typing import Union


class AnimeLink(BaseModel):
    id: Union[str, None]
    url: Union[str, None]


class AnimeData(BaseModel):
    livechart_id: str
    romaji_title: str
    english_title: str
    native_title: str
    alternate_titles: list[str]
    premiere_timestamp: int
    episode: str
    main_title: str
    genres: list[str]
    studio: list[str]
    premiere_date: str
    synopsis: str
    anime_source: str
    anime_episodes: str
    anilist: AnimeLink
    mal: AnimeLink
    anidb: AnimeLink
    animeplanet: AnimeLink
    anisearch: AnimeLink
    kitsu: AnimeLink
    website: AnimeLink
    posters: list[str]


class AnimeTitles(BaseModel):
    romaji: str
    english: str
    native: str


class AnimeInfo(BaseModel):
    posters: list[str]
    rating: str
    titles: AnimeTitles
    premiere: str
    season: str
    website: str
    status: str
    anime_format: Union[str, None] = None
    source: Union[str, None] = None
    episodes: Union[str, None] = None
    run_time: Union[str, None] = None
    description: Union[str, None] = None
    studios: list[str]
    tags: list[str]
    anilist_id: Union[str, None] = None
    mal_id: Union[str, None] = None
    anidb_id: Union[str, None] = None
    animeplanet_id: Union[str, None] = None
    anisearch_id: Union[str, None] = None
    kitsu_id: Union[str, None] = None
