from app.application.interfaces.business_flow_i import FlowRepoInterface
from app.application.usecases.business_flow.dto import FlowStepRequestDTO, FlowStepReplyDTO


class FetchFlowStepUseCase:
    """
    Gets a step by key, gets text from DB, sends result to presentation.
    """

    def __init__(self, repo: FlowRepoInterface, dto: FlowStepRequestDTO):
        self.repo = repo
        self.dto = dto

    async def __call__(self) -> FlowStepReplyDTO:
        response = await self.repo.get_response(flow_name=self.dto.flow_prefix, response_key=self.dto.step_key)
        return response
