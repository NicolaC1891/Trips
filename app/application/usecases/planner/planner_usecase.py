import calendar
from datetime import date, timedelta, datetime

from app.application.interfaces.planner_i import PlannerRepoInterface
from app.infra.logs.logger import logger


class ShowCitiesUseCase:
    def __init__(self, repo: PlannerRepoInterface, region):
        self.repo = repo
        self.region = region

    async def __call__(self):
        cities_dict = await self.repo.get_cities(self.region)
        return dict(sorted(cities_dict.items(), key=lambda item: item[0]))


class AskTripPlannedDateUseCase:

    def __init__(self, prefix: str, year_str: str, month_str: str):
        self.prefix = prefix
        self.year = int(year_str)
        self.month = int(month_str)

    async def execute(self):

        match self.prefix:

            case "today":
                self.year = date.today().year
                self.month = date.today().month

            case "prev":
                self.month -= 1
                if self.month == 0:
                    self.month = 12
                    self.year -= 1

            case "next":
                self.month += 1
                if self.month == 13:
                    self.month = 1
                    self.year += 1

            case _:
                logger.error("ShowCalendar error: unknown prefix")
                raise ValueError("Unknown month prefix")

        days = calendar.Calendar().monthdayscalendar(self.year, self.month)
        return self.year, self.month, days


class ShowTripInfoUseCase:
    def __init__(self, repo, route_service, weather_service, city_from, city_to, trip_date):
        self.repo = repo
        self.route_service = route_service
        self.weather_service = weather_service
        self.city_from = city_from
        self.city_to = city_to
        self.trip_date = trip_date

    async def get_route(self):
        start_lat, start_lon = await self.repo.get_coordinates(self.city_from)
        end_lat, end_lon = await self.repo.get_coordinates(self.city_to)  # list of two floats
        start_coord = [start_lon, start_lat]
        end_coord = [end_lon, end_lat]

        distance, duration = await self.route_service.get_route(start_coord, end_coord)
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        message = (f"<b>Информация о маршруте</b>\n\n"
                   f"Расстояние: <b>{int(distance / 1000)} км.</b>\n"
                   f"Время в пути: <b>{hours}</b> ч. <b>{minutes}</b> мин.")

        return message

    async def get_hotels(self):
        hotels = await self.repo.get_city_details(self.city_to)
        message_hotels = "<b>Рекомендуемые гостиницы</b>\n" + hotels
        return message_hotels

    async def get_weather(self):

        start_date = self.trip_date
        end_date = self.trip_date + timedelta(days=2)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        end_coord = await self.repo.get_coordinates(self.city_to)

        weather_data = await self.weather_service.get_weather(end_coord, start_date_str, end_date_str)

        message = [f"🌞 <b>Прогноз погоды:</b> {self.city_to}\n"]

        if weather_data and "daily" in weather_data and "time" in weather_data["daily"]:
            daily = weather_data["daily"]
            dates = daily["time"]
            t_min = daily.get("temperature_2m_min", [])
            t_max = daily.get("temperature_2m_max", [])
            wind = daily.get("windspeed_10m_max", [])
            precip = daily.get("precipitation_probability_max", [])

            for i in range(len(dates)):
                cur_date = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%d.%m.%Y")
                line = (
                    f"<b>{cur_date}</b>: 🌡 {t_min[i]}…{t_max[i]}°C,\n"
                    f"💨 до {wind[i]} м/с, 🌧 {precip[i]}%"
                )
                message.append(line)
        else:
            message.append("⚠️ Прогноз погоды недоступен на выбранную дату.")

        return "\n".join(message)