from app.utils.exceptions.settlement_exception import SettlementException
from app.utils.exceptions.road_exception import RoadException
from app.game.states.setup.setup_roll_state import SetupRollState


class Game:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.state = SetupRollState()  # Start with setup roll state

        self.current_player_index = 0
        self.current_player_roll = 0

    # State management
    def set_state(self, state):
        self.state = state

    # Player management
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def current_player(self):
        return self.players[self.current_player_index]

    # Command execution
    def execute_command(self, command, player):
        return self.state.execute(command, self, player)

    # Handlers for various game actions
    def handle_dice_roll(self, dice_value: int):
        if self.state.__class__.__name__ == "SetupRollState":
            self.players[self.current_player_index].roll_dice(dice_value)
            return dice_value

        self.players[self.current_player_index].roll_dice(dice_value)
        produced_resources = self.board.produce_resources(dice_value)

        for player in self.players:
            for resource in produced_resources:
                player.add_resource(resource)

    def handle_place_settlement(self, player, node_position):
        board = self.board

        # 1. Node must exist
        if node_position not in board.nodes:
            raise SettlementException("Invalid node position")

        node = board.nodes[node_position]

        # 2. Node must be free
        if node.owner is not None:
            raise SettlementException("Node already occupied")

        node.owner = player.name
        player.add_settlement(node_position)
        player.victory_points += 1

    def handle_place_road(self, player, a, b):
        board = self.board
        key = tuple(sorted((a, b)))

        # 1. Edge must exist
        if key not in board.edges:
            raise RoadException("Invalid edge")

        edge = board.edges[key]

        # 2. Edge must be free
        if edge.owner is not None:
            raise RoadException("Edge already occupied")

        # 3. Must connect to a settlement (simplified rule)
        if a not in player.settlements and b not in player.settlements:
            raise RoadException("Road must connect to a settlement")

        edge.owner = player.name
        player.add_road(a, b)
