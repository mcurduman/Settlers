from engine.game.commands.command import Command


class GetStateCommand(Command):
    def __init__(self, game, **kwargs):
        super().__init__(game)
        self.kwargs = kwargs

    def execute(self, player=None):
        return self.game.handle_get_state(**self.kwargs)
