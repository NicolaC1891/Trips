import random
from datetime import date


class Randomizer:

    def __init__(self, array):
        self.array = array

    def randomize_seed_today(self):
        today_seed = date.today().toordinal()
        random.seed(today_seed)
        random_item = random.choice(self.array)
        return random_item
