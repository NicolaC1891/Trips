import random
from datetime import date

from app.application.interfaces.cat_wisdom_i import ICatWisdomRepo


class GetCatWisdom:
    """
    Random wisdom by id, seed today: all users see the same wisdom, changing daily.
    """

    def __init__(self, repo: ICatWisdomRepo):
        self.repo = repo

    async def __call__(self):
        all_ids = await self.repo.read_all_ids()
        if not all_ids:
            return "Сегодня мудрость в отпуске"
        random_id = self.randomize_id(all_ids)
        wisdom = await self.repo.read_wisdom(random_id)
        if not wisdom:
            wisdom = "Сегодня мудрость в отпуске"
        return wisdom

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
