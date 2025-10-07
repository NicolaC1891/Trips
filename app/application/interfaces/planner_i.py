from abc import ABC, abstractmethod


class PlannerRepoInterface(ABC):

    @abstractmethod
    async def get_cities(self, region):
        pass

    @abstractmethod
    async def get_city_details(self, city):
        pass

    @abstractmethod
    async def get_coordinates(self, city):
        pass


class OpenRouteServiceInterface(ABC):
    @abstractmethod
    async def get_route(self, start_coord, end_coord):
        pass


class OpenMeteoServiceInterface(ABC):
    @abstractmethod
    async def get_weather(self, end_coord, start_date_str, end_date_str):
        pass
