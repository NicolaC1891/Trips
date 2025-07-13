from domain.flow_logic import FlowStepValidator, FlowStep
from features.business_trips.flow_repo_interface import FlowRepoInterface


class FetchFlowStepUseCase:
    """
    Gets a step by key, validates it, gets text from DB, sends result to presentation.
    """

    def __init__(self, flow: dict, step_key: str, validator: FlowStepValidator, repo: FlowRepoInterface):
        self.prefix = flow
        self.step_key = step_key
        self.validator = validator
        self.repo = repo
        self.flow = flow

    async def execute(self) -> FlowStep:

        try:
            step = self.flow[self.step_key]
        except KeyError("Missing key in flow: {e}"):
            raise

        if not self.validator.is_valid_step(step):
            raise ValueError("Invalid flow step")

        response = await self.repo.get_response(step.response_key)
        step.content = response

        return step
