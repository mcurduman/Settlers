from engine.game.commands.command import Command


class EndGameCommand(Command):
    def __init__(self, game, **kwargs):
        super().__init__(game)
        self.kwargs = kwargs

    def execute(self, player=None):
        return self.game.handle_end_game(**self.kwargs)
