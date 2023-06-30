from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import USER_ACCESS_KEY
from database import get_async_session
from exceptions import NoDataException, WrongAccessKeyException
from information.schemas import AvgByDateRequest
from information.utils import get_avg_direction
from station.models import point
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
        station_id = request.get("station_id")
        req_date = request.get("req_date")
        points_query = select(point).where(point.c.station_id == station_id).filter(func.date(point.c.date) == req_date)
        points = await session.execute(points_query)
        points = points.all()
        points_count = len(points)

        if points_count == 0:
            raise NoDataException("No data")

        temperature, wind_direction, wind_speed, air_humidity = 0, 0, 0, 0
        wind_directions = []

        for p in points:
            temperature += p[3]
            wind_directions.append(p[4])
            wind_speed += p[5]
            air_humidity += p[6]

        wind_direction = (get_avg_direction(wind_directions))

        return {
            "status": "success",
            "data": {
                "avg_temperature": temperature / points_count,
                "avg_wind_direction": wind_direction / points_count,
                "avg_wind_speed": wind_speed / points_count,
                "avg_air_humidity": air_humidity / points_count,
            },
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

    except Exception:
        return {
            "status": "error",
            "data": None,
            "details": None,
        }
