from aiogram.fsm.context import FSMContext


class FSMCache:

    def __init__(self, state: FSMContext):
        self.state = state

    async def get_data(self, feature_name: str) -> dict:
        """

        :param feature_name: Name of separate feature to be cached
        :return: dict with data relating to the specific feature
        """
        all_data = await self.state.get_data()  # Getting all data from common cache
        return all_data.get(
            feature_name, {}
        )  # Selecting data relating to the feature. SAFELY!!!

    async def set_data(self, feature_name: str, data: dict):
        all_data = await self.state.get_data()  # Getting all data from common cache
        all_data[feature_name] = data
        await self.state.set_data(all_data)  # Replace all feature-related cache

    async def update_data(self, feature_name: str, **kwargs):
        all_data = await self.state.get_data()  # Getting all data from common cache
        feature_data = all_data.get(feature_name, {})
        feature_data.update(kwargs)  # updating dict-like feature cash with kwargs dict
        all_data[feature_name] = feature_data
        await self.state.set_data(all_data)

    async def clear_data(self, feature_name: str):
        all_data = await self.state.get_data()
        all_data.pop(feature_name, None)
        await self.state.set_data(all_data)
