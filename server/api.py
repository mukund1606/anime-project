from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.liveChartRoute import router as LiveChartRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def home_page():
    return {"message": "Welcome to my anime scraper, use the /docs route to proceed"}


app.include_router(LiveChartRouter, prefix="/livechart")
