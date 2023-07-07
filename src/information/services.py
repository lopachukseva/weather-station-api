from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import NoDataException
from information.utils import get_avg_direction
from station.models import point


async def get_average_values_by_date_and_station(station_id: int, req_date: date, session: AsyncSession):
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
        "avg_temperature": temperature / points_count,
        "avg_wind_direction": wind_direction,
        "avg_wind_speed": wind_speed / points_count,
        "avg_air_humidity": air_humidity / points_count,
    }
