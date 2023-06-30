from fastapi import FastAPI

from information.router import router as router_information
from station.router import router as router_station

app = FastAPI(name="Weather station")

app.include_router(router_station)
app.include_router(router_information)
