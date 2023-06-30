from fastapi import FastAPI
from station.router import router as router_station
from information.router import router as router_information

app = FastAPI(name="Weather station")

app.include_router(router_station)
app.include_router(router_information)
