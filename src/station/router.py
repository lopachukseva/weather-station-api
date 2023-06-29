from fastapi import APIRouter, Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from station.models import station, point
from station.schemas import NewPoint, NewStation, AccessKey
from config import STATION_ACCESS_KEY, USER_ACCESS_KEY

router = APIRouter(
    prefix="/station",
    tags=["Station"],
)


@router.post("/new-point")
async def add_point(new_point: NewPoint, access_key: AccessKey, session: AsyncSession = Depends(get_async_session)):
    access_key = access_key.dict()["key"]
    if access_key == STATION_ACCESS_KEY:
        stmt = insert(point).values(**new_point.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        return {"status": "not allowed"}


@router.post("/new-station")
async def add_station(new_station: NewStation, access_key: AccessKey, session: AsyncSession = Depends(get_async_session)):
    access_key = access_key.dict()["key"]
    if access_key == USER_ACCESS_KEY:
        stmt = insert(station).values(**new_station.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        return {"status": "not allowed"}
