from fastapi import APIRouter
from utils.LiveChart import LiveChart

router = APIRouter()
liveChart = LiveChart()


@router.get("/", tags=["LiveChart API"])
async def live_anime_schedule() -> dict:
    return liveChart.timetable()
