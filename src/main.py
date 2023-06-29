from fastapi import FastAPI
from station.router import router as router_station

app = FastAPI(name="Weather station")

app.include_router(router_station)
