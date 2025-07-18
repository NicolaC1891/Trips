from features.business_trips.flow_repo_interface import FlowRepoInterface


class ShowMainMenuUseCase:
    def __init__(self, tg_user, repo: FlowRepoInterface):
        self.tg_user = tg_user
        self.repo = repo

    async def execute(self) -> str:
        name = self.tg_user.full_name or "коллега"
        response = await self.repo.get_response("to_main")
        return f"Здравствуйте, <b>{name}</b>!\n\n{response}"


class ShowSimpleMenuOptionUseCase:

    def __init__(self, repo: FlowRepoInterface, response_key: str):
        self.repo = repo
        self.response_key = response_key

    async def execute(self) -> str:
        response = await self.repo.get_response(self.response_key)
        return response
