import random
from datetime import date

from app.application.interfaces.business_flow_i import FlowRepoInterface
from app.application.interfaces.cat_wisdom_i import CatWisdomRepoInterface
from app.application.usecases.office_cat.dto import OfficeCatReplyDTO
from app.infra.repositories.business_flow_r import FlowRepo
from app.application.usecases.business_flow.dto import FlowStepRequestDTO


class ShowOfficeCatUseCase:
    """
    Gets message template from DB, adds random wisdom into placeholder.
    Random wisdom by id, seed today: all users see the same wisdom, changing daily.
    """

    def __init__(self, message_repo: FlowRepoInterface, wisdom_repo: CatWisdomRepoInterface, dto: FlowStepRequestDTO):
        self.message_repo = message_repo
        self.wisdom_repo = wisdom_repo
        self.dto = dto

    async def __call__(self):
        """
        Executes the usecase
        :return: DTO
        """
        wisdom = await self.get_random_wisdom()
        reply = await self.get_response()
        reply.response = reply.response.format(wisdom_text=wisdom)
        return reply

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
        reply = await self.message_repo.get_response(flow_name=self.dto.flow_prefix, response_key=self.dto.step_key)
        return reply

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
