from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import USER_ACCESS_KEY
from database import get_async_session
from exceptions import NoDataException, WrongAccessKeyException
from information.schemas import AvgByDateRequest, LastPointStationRequest
from information.services import get_date_avg_data, get_last_station_point_data
from station.schemas import AccessKey

router = APIRouter(
    prefix="/info",
    tags=["Information"],
)


@router.post("/get-date-avg")
async def get_date_avg(request_data: AvgByDateRequest, access_key: AccessKey,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        access_key = access_key.dict()["key"]
        if access_key != USER_ACCESS_KEY:
            raise WrongAccessKeyException()
        request = request_data.dict()
        station_id, req_date = request.get("station_id"), request.get("req_date")
        data = await get_date_avg_data(station_id, req_date, session)

        return {
            "status": "success",
            "data": data,
            "details": None,
        }

    except WrongAccessKeyException:
        return {
            "status": "error",
            "data": None,
            "details": "wrong access code",
        }

    except NoDataException:
        return {
            "status": "error",
            "data": None,
            "details": "no data for this day",
        }


@router.post("/get-last-station-point")
async def get_last_station_point(request_data: LastPointStationRequest, access_key: AccessKey,
                                 session: AsyncSession = Depends(get_async_session)):
    try:
        access_key = access_key.dict()["key"]
        if access_key != USER_ACCESS_KEY:
            raise WrongAccessKeyException()
        request = request_data.dict()
        station_id = request.get("station_id")
        data = await get_last_station_point_data(station_id, session)

        return {
            "status": "success",
            "data": data,
            "details": None,
        }

    except WrongAccessKeyException:
        return {
            "status": "error",
            "data": None,
            "details": "wrong access code",
        }

    except NoDataException:
        return {
            "status": "error",
            "data": None,
            "details": "no data for this day",
        }
