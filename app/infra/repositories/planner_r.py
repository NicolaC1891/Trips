import aiohttp
from sqlalchemy import select

from app.application.interfaces.planner_i import PlannerRepoInterface
from app.config.settings import config
from app.infra.rel_db.SQLA import PlannerCities


class PlannerRepo(PlannerRepoInterface):
    def __init__(self, session):
        self.session = session

    async def get_cities(self, region):
        statement = select(PlannerCities).where(PlannerCities.region == region)
        result = await self.session.execute(statement)
        record = result.scalars()
        cities_dict = {line.cityname: line.city for line in record}
        return cities_dict

    async def get_city_details(self, city):
        statement = select(PlannerCities).where(PlannerCities.cityname == city)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        hotels = record.hotel
        return hotels

    async def get_coordinates(self, city):
        statement = select(PlannerCities).where(PlannerCities.cityname == city)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        lat, lon = record.lat, record.lon
        return lat, lon


class OpenRouteService:

    @staticmethod
    async def get_route(start_coord, end_coord):
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {"Authorization": config.ROUTE.ROUTE_TOKEN.get_secret_value(),
                   "Content-Type": "application/json"}
        body = {"coordinates": [start_coord, end_coord]}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as response:
                data = await response.json()
                distance = data['routes'][0]['summary']['distance']  # meters
                duration = data['routes'][0]['summary']['duration']  # seconds

        return distance, duration


class OpenMeteoService:

    async def get_weather(self, end_coord, start_date_str, end_date_str):
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={end_coord[0]}&longitude={end_coord[1]}"
            "&daily=temperature_2m_min,temperature_2m_max,precipitation_sum,"
            "precipitation_probability_max,windspeed_10m_max"
            f"&start_date={start_date_str}&end_date={end_date_str}"
            "&timezone=auto"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                weather_data = await response.json()

        return weather_data
