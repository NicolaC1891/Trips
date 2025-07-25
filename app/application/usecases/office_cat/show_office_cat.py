import random
from datetime import date

from app.application.interfaces.menu_item_i import MenuItemRepoInterface
from app.application.usecases.office_cat.dto import OfficeCatReplyDTO, OfficeCatRequestDTO
from app.application.interfaces.cat_wisdom_i import CatWisdomRepoInterface


class ShowOfficeCatUseCase:
    """
    Gets message template from DB, adds random wisdom into placeholder.
    Random wisdom by id, seed today: all users see the same wisdom, changing daily.
    """

    def __init__(
            self,
            wisdom_repo: CatWisdomRepoInterface,
            menu_item_repo: MenuItemRepoInterface,
            dto: OfficeCatRequestDTO
    ):
        self.wisdom_repo = wisdom_repo
        self.menu_item_repo = menu_item_repo
        self.dto = dto

    async def __call__(self) -> OfficeCatReplyDTO:
        """
        Executes the usecase
        :return: DTO
        """
        wisdom = await self.get_random_wisdom()
        response = await self.get_response()
        message = response.format(wisdom_text=wisdom)
        return OfficeCatReplyDTO(reply=message)

    async def get_random_wisdom(self) -> str:
        """
        Gets all available wisdom ids from DB, randomly selects one, fetches the wisdom from DB
        :return: Wisdom string
        """
        all_ids = await self.wisdom_repo.read_all_ids()
        if not all_ids:
            return "Сегодня мудрость в отпуске"
        random_id = self.randomize_id(all_ids)
        response = await self.wisdom_repo.read_wisdom(random_id)
        if not response:
            response = "Сегодня мудрость в отпуске"
        return response

    async def get_response(self) -> str:
        """
        Fetches template message from DB
        :return: Message string
        """
        response = await self.menu_item_repo.get_response(self.dto.response_key)
        if not response:
            response = "Произошла ошибка. Попробуйте позже"
        return response

    @staticmethod
    def randomize_id(ids) -> int:
        """
        Randomizes id from the list.
        :param ids: List with all wisdom ids from DB
        :return: Randomly selected ID.
        """
        today_hash = date.today().toordinal()
        random.seed(today_hash)
        random_id = random.choice(ids)
        return random_id
