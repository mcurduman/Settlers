from abc import ABC, abstractmethod


class GameState(ABC):
    @abstractmethod
    def execute(self, command, game, player):
        pass
