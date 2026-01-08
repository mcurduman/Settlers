class EndTurnCommand:
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.handle_end_turn()
