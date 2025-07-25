from app.application.entities.flow_step_entity import FlowStepValidator
from app.application.interfaces.business_flow_i import FlowRepoInterface
from app.application.usecases.business_flow.dto import FlowStepRequestDTO, FlowStepReplyDTO
from app.application.usecases.business_flow.flows.flow_resolver import FlowResolver


class FetchFlowStepUseCase:
    """
    Gets a step by key, validates it, gets text from DB, sends result to presentation.
    """

    def __init__(self, repo: FlowRepoInterface, validator: FlowStepValidator, dto: FlowStepRequestDTO):
        self.repo = repo
        self.validator = validator
        self.dto = dto


    async def __call__(self) -> FlowStepReplyDTO:
        flow: dict = FlowResolver()[self.dto.flow_prefix]
        step = flow[self.dto.step_key]

        response = await self.repo.get_response(step.response_key)

        if step.children:
            child_labels = [flow[child].label for child in step.children]
        else:
            child_labels = None

        return FlowStepReplyDTO(flow_step=step, child_labels=child_labels, reply=response)
