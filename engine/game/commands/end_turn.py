# EndTurnCommand


class EndTurnCommand:
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.end_turn()
