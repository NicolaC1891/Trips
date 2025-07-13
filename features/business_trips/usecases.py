from features.business_trips.flows.flow_resolver import FlowResolver
from common.logger.logger import logger


class FetchFlowStepUseCase:
    """
    Gets a step by key, validates it, gets text from DB, sends result to presentation.
    """
    def __init__(self, flow, step_key, validator, repo):
        self.prefix = flow
        self.step_key = step_key
        self.validator = validator
        self.repo = repo
        self.flow = flow

    async def execute(self):

        try:
            step = self.flow[self.step_key]
        except KeyError("Missing key in flow: {e}"):
            raise

        if not self.validator.is_valid_step(step):
            raise ValueError("Invalid flow step")

        response = await self.repo.get_response(step.response_key)
        step.content = response

        return step
