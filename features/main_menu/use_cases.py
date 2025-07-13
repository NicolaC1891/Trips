

class ShowMainMenuUseCase:
    def __init__(self, tg_user, repo):
        self.tg_user = tg_user
        self.repo = repo

    async def execute(self):
        name = self.tg_user.full_name or 'коллега'
        response = await self.repo.get_response('to_main')
        return f"Здравствуйте, <b>{name}</b>!\n\n{response}"


class ShowSimpleMenuOptionUseCase:

    def __init__(self, repo, response_key):
        self.repo = repo
        self.response_key = response_key

    async def execute(self):
        response = await self.repo.get_response(self.response_key)
        return response
