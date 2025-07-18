from domain.random_picker import RandomItemPicker


class GetCatWisdomUseCase:

    def __init__(self, wisdom_repo, message_repo, response_key):
        self.wisdom_repo = wisdom_repo
        self.message_repo = message_repo
        self.response_key = response_key

    async def execute(self) -> str:
        all_ids = await self.wisdom_repo.read_all_ids()
        random_id = RandomItemPicker(all_ids).pick_by_seed_today()
        wisdom = await self.wisdom_repo.read_wisdom(random_id)
        message = await self.message_repo.get_response(self.response_key)
        wisdom_message = f"{message}\n{wisdom}"
        return wisdom_message
