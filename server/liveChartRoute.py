from fastapi import APIRouter
from utils.LiveChart import LiveChart

router = APIRouter()
liveChart = LiveChart()


@router.get("/timetable", tags=["LiveChart API"])
async def live_anime_timetable() -> dict:
    return liveChart.timetable()


@router.get("/anime/{anime_id}", tags=["LiveChart API"])
async def live_anime(anime_id: str) -> dict:
    return liveChart.anime_data(anime_id)


@router.get("/schedule", tags=["LiveChart API"])
async def live_anime_schedule() -> dict:
    return liveChart.schedule()
