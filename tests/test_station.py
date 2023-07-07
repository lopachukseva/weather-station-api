from datetime import date

from httpx import AsyncClient

from src.config import STATION_ACCESS_KEY, USER_ACCESS_KEY


async def test_add_station(ac: AsyncClient):
    response = await ac.post("/station/new-station", json={
        "new_station": {
            "name": "Mondy",
            "city": "Saint-Petersburg",
            "lat": 10,
            "lon": 20
        },
        "access_key": {
            "key": USER_ACCESS_KEY
        }
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_add_point(ac: AsyncClient):
    response = await ac.post("/station/new-point", json={
        "new_point": {
            "station_id": 1,
            "temperature": 10,
            "wind_direction": 90,
            "wind_speed": 4,
            "air_humidity": 34
        },
        "access_key": {
            "key": STATION_ACCESS_KEY
        }
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_stations(ac: AsyncClient):
    response = await ac.post("/station/stations", json={
        "key": USER_ACCESS_KEY
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_date_avg(ac: AsyncClient):
    response = await ac.post("/info/get-date-avg", json={
        "request_data": {
            "station_id": 1,
            "req_date": str(date.today())
        },
        "access_key": {
            "key": USER_ACCESS_KEY
        }
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
