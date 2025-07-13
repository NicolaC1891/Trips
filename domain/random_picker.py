import random
from datetime import date
from typing import Sequence, Any


class RandomItemPicker:
    """
    Just a randomizer
    """

    def __init__(self, items: Sequence) -> None:
        self.items = items

    def pick_by_seed_today(self) -> Any:
        today_hash = date.today().toordinal()
        random.seed(today_hash)
        item = random.choice(self.items)
        return item
