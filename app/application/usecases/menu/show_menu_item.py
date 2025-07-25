from app.application.interfaces.menu_item_i import MenuItemRepoInterface
from app.application.usecases.menu.dto import ShowMenuItemRequestDTO, ShowMenuItemReplyDTO


class ShowMenuItemUseCase:

    def __init__(self, repo: MenuItemRepoInterface, dto: ShowMenuItemRequestDTO):
        self.repo = repo
        self.dto = dto

    async def __call__(self) -> ShowMenuItemReplyDTO:
        response = await self.repo.get_response(self.dto.response_key)
        if not response:
            return ShowMenuItemReplyDTO(reply="Произошла ошибка. Попробуйте позже.")
        return ShowMenuItemReplyDTO(reply=response)
