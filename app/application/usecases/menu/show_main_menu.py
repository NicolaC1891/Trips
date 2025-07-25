from app.application.interfaces.menu_item_i import MenuItemRepoInterface
from app.application.usecases.menu.dto import ShowMenuItemRequestDTO, ShowMenuItemReplyDTO


class ShowMainMenuUseCase:
    def __init__(self, tg_user, repo: MenuItemRepoInterface, dto: ShowMenuItemRequestDTO):
        self.tg_user = tg_user
        self.repo = repo
        self.dto = dto

    async def __call__(self) -> ShowMenuItemReplyDTO:
        name = self.tg_user.full_name or "коллега"
        response = await self.repo.get_response(self.dto.response_key)
        if not response:
            return ShowMenuItemReplyDTO(reply="Произошла ошибка. Попробуйте позже.")
        message = response.format(username=name)
        return ShowMenuItemReplyDTO(reply=message)
