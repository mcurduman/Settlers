from engine.game.players.player import Player


class AIPlayer(Player):
    def __init__(self, name="AI"):
        super().__init__(name=name)

    def is_ai(self) -> bool:
        return True
