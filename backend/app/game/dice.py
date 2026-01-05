import random


class Dice:
    @staticmethod
    def roll() -> int:
        return random.randint(1, 6)
