from datetime import date

from pydantic import BaseModel


class AvgByDateRequest(BaseModel):
    station_id: int
    req_date: date
