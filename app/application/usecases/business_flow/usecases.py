from app.application.interfaces.business_flow_i import IFlowRepo


class GetFlowStep:
    """
    Gets a step by key, gets text from DB, sends result to presentation.
    """

    def __init__(self, repo: IFlowRepo, table_name, step_key):
        self.repo = repo
        self.table_name = table_name
        self.step_key = step_key

    async def __call__(self):
        step = await self.repo.get_response(table_name=self.table_name, step_key=self.step_key)
        return step
