from typing import Optional, List

from pydantic import BaseModel


class NewStation(BaseModel):
    name: str
    city: str


class NewPoint(BaseModel):
    station_id: int
    temperature: int
    wind_direction: int
    wind_speed: int
    air_humidity: int


class AccessKey(BaseModel):
    key: str


class Station(BaseModel):
    id: int
    name: str
    city: str

    class Config:
        orm_mode = True


class StationResponse(BaseModel):
    status: str
    data: Optional[List[Station]]
    details: Optional[str]
