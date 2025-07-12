from features.business_trips.flows.flow_resolver import FlowResolver
from common.logger.logger import logger


class FetchFlowStepUseCase:
    """
    Gets a step by key, validates it, gets text from DB, sends result to presentation.
    """
    def __init__(self, prefix, step_key, validator, repo):
        self.prefix = prefix
        self.step_key = step_key
        self.validator = validator
        self.repo = repo
        self.step_flow = FlowResolver()

    async def execute(self):
        flow = self.step_flow[self.prefix]

        try:
            step = flow[self.step_key]
        except KeyError as e:
            logger.error(f"Dict key missing: {e}")
            raise ValueError('No step available')

        if not self.validator.is_valid_step(step):
            logger.error("Step is missing response_key or label")
            raise ValueError("Step is not valid")

        response = await self.repo.get_response(step.response_key)
        step.content = response

        return flow, step
