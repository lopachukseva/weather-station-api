from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import STATION_ACCESS_KEY, USER_ACCESS_KEY
from database import get_async_session
from exceptions import WrongAccessKeyException
from station.models import point, station
from station.schemas import AccessKey, NewPoint, NewStation, StationResponse

router = APIRouter(
    prefix="/station",
    tags=["Station"],
)


@router.post("/new-point")
async def add_point(new_point: NewPoint, access_key: AccessKey, session: AsyncSession = Depends(get_async_session)):
    try:
        access_key = access_key.dict()["key"]
        if access_key != STATION_ACCESS_KEY:
            raise WrongAccessKeyException()
        stmt = insert(point).values(**new_point.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except WrongAccessKeyException:
        return {
            "status": "error",
            "data": None,
            "details": "wrong access code",
        }
    except Exception:
        return {
            "status": "error",
            "data": None,
            "details": None,
        }


@router.post("/new-station")
async def add_station(new_station: NewStation, access_key: AccessKey,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        access_key = access_key.dict()["key"]
        if access_key != USER_ACCESS_KEY:
            raise WrongAccessKeyException()
        stmt = insert(station).values(**new_station.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except WrongAccessKeyException:
        return {
            "status": "error",
            "data": None,
            "details": "wrong access code",
        }


@router.post("/stations", response_model=StationResponse)
async def get_stations(access_key: AccessKey, session: AsyncSession = Depends(get_async_session)):
    try:
        access_key = access_key.dict()["key"]
        if access_key != USER_ACCESS_KEY:
            raise WrongAccessKeyException()
        stations_query = select(station)
        stations = await session.execute(stations_query)
        return {
            "status": "success",
            "data": stations.all(),
            "details": None,
        }
    except WrongAccessKeyException:
        return {
            "status": "error",
            "data": None,
            "details": "wrong access code",
        }
