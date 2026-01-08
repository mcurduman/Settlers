from engine.game.players.player import Player


class HumanPlayer(Player):
    def __init__(self, name="Human"):
        super().__init__(name=name)
