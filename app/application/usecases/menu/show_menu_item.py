from app.application.interfaces.menu_item_i import MenuItemRepoInterface

class ShowMenuItemUseCase:

    def __init__(self, repo: MenuItemRepoInterface, step_key):
        self.repo = repo
        self.step_key = step_key

    async def __call__(self):
        reply = await self.repo.get_response(self.step_key)
        return reply
