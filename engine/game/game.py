from engine.game.states.setup.setup_roll_state import SetupRollState
from engine.game.strategies.strategy_factory import get_ai_strategy
from engine.utils.exceptions.not_enough_resources_for_trade_exception import \
    NotEnoughResourcesForTradeException
from engine.utils.exceptions.road_exception import RoadException
from engine.utils.exceptions.settlement_exception import SettlementException


class Game:
    def __init__(self, players, board, difficulty=None):
        self.players = players
        self.board = board
        self.state = SetupRollState()  # Start with setup roll states

        self.setup_order = players * 2
        self.setup_index = 0

        self.current_player_index = 0
        self.current_player_roll = 0

        self.difficulty = difficulty
        self.ai_strategy = get_ai_strategy(difficulty) if difficulty else None
        self.ai_action_description = None
        self.longest_road_holder = None

        self.winner = None
        self.error = None

    # State management
    def set_state(self, state):
        self.state = state

    def _state_specific_extra(self):
        extra = {}
        if self.state.get_name() == "SetupRollState":
            extra["rolls"] = {
                player.name: roll for player, roll in self.state.rolls.items()
            }
        elif self.state.get_name() == "SetupPlaceSettlementState":
            extra["setup_phase"] = "placing settlements"
        elif self.error is not None:
            extra["error"] = self.error
            self.error = None
        return extra

    def get_state(self, extra: dict | None = None):
        state = {
            "state": self.state.get_name(),
            "board": {
                "tiles": [tile.model_dump() for tile in self.board.tiles],
                "nodes": [node.model_dump() for node in self.board.nodes.values()],
                "edges": [edge.model_dump() for edge in self.board.edges.values()],
            },
            "players": [
                {
                    "name": p.name,
                    "victory_points": p.victory_points,
                    "resources": {r.value: v for r, v in p.resources.items()},
                    "settlements": list(p.settlements),
                    "roads": list(p.roads),
                    "longest_road": self.board.longest_road(p),
                    "last_dice_roll": p.last_dice_roll,
                    "is_ai": p.is_ai(),
                }
                for p in self.players
            ],
            "current_player": self.current_player().name,
            "longest_road_holder": (
                self.longest_road_holder.name if self.longest_road_holder else None
            ),
            "winner": self.winner if self.winner else None,
            "ai_action_description": (
                self.ai_action_description if self.ai_action_description else None
            ),
        }

        state_specific = self._state_specific_extra()
        state.update(state_specific)
        if extra:
            state.update(extra)
        return state

    # Player management
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def check_if_won(self):
        for player in self.players:
            if player.victory_points >= 5:
                self.winner = player.name
                return player
        return None

    def current_player(self):
        return self.players[self.current_player_index]

    def _update_longest_road_holder(self):
        MIN_LENGTH = 4

        road_lengths = {
            player: self.board.longest_road(player) for player in self.players
        }

        eligible = {p: l for p, l in road_lengths.items() if l >= MIN_LENGTH}
        if not eligible:
            if self.longest_road_holder:
                self.longest_road_holder.victory_points -= 1
                self.longest_road_holder = None
            return

        max_length = max(eligible.values())
        contenders = [p for p, l in eligible.items() if l == max_length]

        if self.longest_road_holder in contenders:
            return

        if self.longest_road_holder:
            holder_length = road_lengths[self.longest_road_holder]
            if holder_length >= MIN_LENGTH and holder_length == max_length:
                return
            self.longest_road_holder.victory_points -= 1

        new_holder = contenders[0]
        new_holder.victory_points += 1
        self.longest_road_holder = new_holder

    def execute_command(self, command, player):
        return self.state.execute(command, self, player)

    def handle_end_turn(self):
        self.next_player()

    def handle_dice_roll(self, dice_value: int):
        if self.state.get_name() == "SetupRollState":
            self.players[self.current_player_index].roll_dice(dice_value)
            return dice_value

        current_player = self.players[self.current_player_index]
        current_player.roll_dice(dice_value)
        for player in self.players:
            produced_resources = self.board.produce_resources(dice_value, player.name)
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

        # 3. If in PlayingPlaceSettlementState, must be adjacent to player's road
        if self.state.get_name() == "PlayingPlaceSettlementState":
            if not self.board.valid_settlement_node(node_position, player):
                raise SettlementException(
                    "Settlement must be adjacent to player's road"
                )
            player.remove_resource_for_settlement()

        # 4.Ifplayer is ai and in PlayingMainState, remove resources
        if self.state.get_name() == "PlayingMainState" and player.name.lower() == "ai":
            player.remove_resource_for_settlement()

        node.owner = player.name
        player.add_settlement(node_position)
        player.victory_points += 1
        self._update_longest_road_holder()

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

        # 3. If in SetupPlaceRoadState, must connect to a settlement (simplified rule)
        if (
            a not in player.settlements
            and b not in player.settlements
            and self.state.get_name() == "SetupPlaceRoadState"
        ):
            raise RoadException("Road must connect to a settlement")

        if self.state.get_name() == "PlayingPlaceRoadState":
            if not board.edge_connected_to_network(edge, player):
                raise RoadException("Road must connect to existing road network")
            player.remove_resource_for_road()
            self._update_longest_road_holder()

        if self.state.get_name() == "PlayingMainState" and player.name.lower() == "ai":
            player.remove_resource_for_road()

        edge.owner = player.name
        player.add_road(a, b)
        self._update_longest_road_holder()

        # If in SetupPlaceRoadState, advance setup index and player
        if self.state.get_name() == "SetupPlaceRoadState":
            self.setup_index += 1
            self.next_player()

    def handle_trade_with_bank(self, player, give_resource, receive_resource, rate):
        if give_resource == receive_resource:
            raise ValueError("Cannot trade the same resource type")

        if player.resources.get(give_resource, 0) < rate:
            raise NotEnoughResourcesForTradeException(
                f"Not enough resources of type {give_resource} to trade with bank"
            )

        player.remove_resource(give_resource, rate)
        player.add_resource(receive_resource, 1)

    def handle_get_state(self, **kwargs):
        return self.get_state()
