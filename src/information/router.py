from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import USER_ACCESS_KEY
from database import get_async_session
from exceptions import NoDataException, WrongAccessKeyException
from information.schemas import AvgByDateRequest
from information.services import get_average_values_by_date_and_station
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
        data = await get_average_values_by_date_and_station(station_id, req_date, session)

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
