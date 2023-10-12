from fastapi import FastAPI
from server.liveChartRoute import router as LiveChartRouter

app = FastAPI()


@app.get("/", tags=["Root"])
async def home_page():
    return {"message": "Welcome to my anime scraper, use the /docs route to proceed"}


app.include_router(LiveChartRouter, prefix="/livechart")
