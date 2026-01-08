from abc import ABC, abstractmethod


class GameState(ABC):
    @abstractmethod
    def execute(self, command, game, player):
        pass

    def get_name(self):
        return self.__class__.__name__
