from aiogram.fsm.context import FSMContext


class FSMCache:

    def __init__(self, state: FSMContext) -> None:
        self.state = state

    async def create(self, feature_name: str, data: dict) -> None:
        all_data = await self.state.get_data()
        all_data[feature_name] = data
        await self.state.set_data(all_data)

    async def read(self, feature_name: str) -> dict:
        all_data = await self.state.get_data()
        return all_data.get(
            feature_name, {}
        )

    async def update(self, feature_name: str, **kwargs) -> None:
        all_data = await self.state.get_data()
        feature_data = all_data.get(feature_name, {})
        feature_data.update(kwargs)
        all_data[feature_name] = feature_data
        await self.state.set_data(all_data)

    async def delete(self, feature_name: str) -> None:
        all_data = await self.state.get_data()
        all_data.pop(feature_name, None)
        await self.state.set_data(all_data)

    async def delete_except(
        self, *preserve_keys: str
    ):  # For clearing except preloaded cache
        all_data = await self.state.get_data()
        new_data = {
            key: value for key, value in all_data.items() if key in preserve_keys
        }
        await self.state.set_data(new_data)
