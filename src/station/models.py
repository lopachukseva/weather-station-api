from datetime import datetime

from sqlalchemy import Table, Column, SmallInteger, Integer, String, ForeignKey, MetaData, TIMESTAMP

metadata = MetaData()

station = Table(
    "station",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("city", String, nullable=False),
)

point = Table(
    "point",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("station_id", Integer, ForeignKey(station.c.id)),
    Column("date", TIMESTAMP, default=datetime.utcnow),
    Column("temperature", SmallInteger, nullable=False),
    Column("wind_direction", SmallInteger, nullable=False),
    Column("wind_speed", SmallInteger, nullable=False),
    Column("air_humidity", SmallInteger, nullable=False),
)
