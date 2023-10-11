from app.utils.livechart import LiveChart
from fastapi import FastAPI

liveChart = LiveChart()
app = FastAPI()


@app.get("/timetable")
def timetable():
    return liveChart.timetable()
