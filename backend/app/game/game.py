class Game:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.state = None

    def set_state(self, state):
        self.state = state

    def execute_command(self, command, player):
        return self.state.execute(command, self, player)

    def handle_dice_roll(self, dice_value: int):
        produced_resources = self.board.produce_resources(dice_value)

        for player in self.players:
            for resource in produced_resources:
                player.add_resource(resource)

    def handle_place_settlement(self, player, position):
        # TODO: Implement actual placement logic (update board, player state, etc.)
        # Exemplu simplu: crește punctele de victorie
        player.victory_points += 1
        # Poți adăuga aici logica de plasare pe board
