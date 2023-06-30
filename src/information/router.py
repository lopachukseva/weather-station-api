from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from config import STATION_ACCESS_KEY, USER_ACCESS_KEY
from database import get_async_session
from information.schemas import AvgByDateRequest
from exceptions import NoDataException, WrongAccessCodeException
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
            raise WrongAccessCodeException()
        request = request_data.dict()
        station_id = request.get("station_id")
        req_date = request.get("req_date")
        points_query = select(point).where(point.c.station_id == station_id).filter(func.date(point.c.date) == req_date)
        points = await session.execute(points_query)
        points = points.all()
        count, temperature, wind_direction, wind_speed, air_humidity = 0, 0, 0, 0, 0
        wind_directions = []

        if len(points) == 0:
            raise NoDataException("No data")

        for p in points:
            count += 1
            temperature += p[3]
            wind_directions.append(p[4])
            wind_speed += p[5]
            air_humidity += p[6]

        wind_direction = (get_avg_direction(wind_directions))

        return {
            "status": "success",
            "data": {
                "avg_temperature": temperature / count,
                "avg_wind_direction": wind_direction / count,
                "avg_wind_speed": wind_speed / count,
                "avg_air_humidity": air_humidity / count,
            },
            "details": None,
        }

    except WrongAccessCodeException:
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
