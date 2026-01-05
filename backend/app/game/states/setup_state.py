from app.game.states.game_state import GameState


class SetupState(GameState):
    def execute(self, command, game, player):
        from app.game.commands.place_settlement import PlaceSettlementCommand

        if isinstance(command, PlaceSettlementCommand):
            return command.execute(game, player)

        raise Exception("Only settlement placement allowed in setup")
