from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from utils.LiveChart import LiveChart

router = APIRouter()
liveChart = LiveChart()

headers = {
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "maxage=30, s-maxage=30, stale-while-revalidate",
}


@router.get("/timetable", tags=["LiveChart API"], status_code=200)
async def live_anime_timetable(response: Response) -> dict:
    try:
        content = liveChart.timetable()
        return JSONResponse(content=content, headers=headers)
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return JSONResponse(
            content={"message": "LiveChart is down"}, headers=headers, status_code=503
        )


@router.get("/anime/{anime_id}", tags=["LiveChart API"], status_code=200)
async def live_anime(anime_id: str, response: Response) -> dict:
    try:
        content = liveChart.anime_data(anime_id)
        return JSONResponse(content=content, headers=headers)
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return JSONResponse(
            content={"message": "LiveChart is down"}, headers=headers, status_code=503
        )


@router.get("/schedule", tags=["LiveChart API"], status_code=200)
async def live_anime_schedule(response: Response) -> dict:
    try:
        content = liveChart.schedule()
        return JSONResponse(content=content, headers=headers)
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return JSONResponse(
            content={"message": "LiveChart is down"}, headers=headers, status_code=503
        )
