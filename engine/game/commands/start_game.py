from engine.game.commands.command import Command


class StartGameCommand(Command):
    def __init__(self, game, **kwargs):
        super().__init__(game)
        self.kwargs = kwargs

    def execute(self, player=None):
        return self.game.handle_start_game(**self.kwargs)
