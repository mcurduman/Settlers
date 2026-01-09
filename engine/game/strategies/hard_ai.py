import math

from engine.game.strategies.ai_helper import (
    edges_touching_network,
    free_edges,
    is_valid_setup_settlement_node,
    can_try_road,
    can_try_settlement,
    get_player_resources,
)
from engine.game.strategies.strategy_ai import StrategyAI


DICE_SCORE = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}


class HardAIStrategy(StrategyAI):
    """
    Advanced AI strategy with persistent planning, setup expansion,
    and goal-driven settlement construction.
    """

    def __init__(self):
        """Initialize internal AI state."""
        self.current_target = None
        self.setup_done = False

    def choose_action(self, game_state, player):
        """
        Decide the next action for the AI based on the current game state.
        """
        state = game_state["state"]

        if state in ("SetupRollState", "PlayingRollState"):
            return self._handle_roll_state()

        if state == "SetupPlaceSettlementState":
            return self._handle_setup_place_settlement(game_state)

        if state == "SetupPlaceRoadState":
            return self._handle_setup_place_road(game_state, player)

        if state == "PlayingMainState":
            return self._handle_playing_main(game_state, player)

        if state == "PlayingPlaceRoadState":
            return self._handle_playing_place_road(game_state, player)

        return {"command": "end_turn", "kwargs": {}}

    def _handle_roll_state(self):
        """Handle dice roll states."""
        return {"command": "roll_dice", "kwargs": {}}

    def _handle_setup_place_settlement(self, game_state):
        """Place the initial settlement during setup."""
        node = self.pick_best_node(game_state)
        return {"command": "place_settlement", "kwargs": {"position": node}}

    def _handle_setup_place_road(self, game_state, player):
        """Place the initial road during setup."""
        target = self.pick_setup_target_node(game_state, player)

        if target:
            edge = self.pick_road_towards_target(game_state, player, target)
            if edge:
                return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

        edge = self.pick_any_setup_road(game_state, player)
        if edge:
            return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

        return {"command": "end_turn", "kwargs": {}}

    def _handle_playing_main(self, game_state, player):
        """Handle the main playing phase."""
        if not self.setup_done:
            self.current_target = None
            self.setup_done = True

        return self._play_main(game_state, player)

    def _handle_playing_place_road(self, game_state, player):
        """Handle forced road placement during playing."""
        target = self.choose_target_node(game_state, player)
        if not target:
            return {"command": "end_turn", "kwargs": {}}

        edge = self.pick_road_towards_target(game_state, player, target)
        if not edge:
            return {"command": "end_turn", "kwargs": {}}

        return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

    def _play_main(self, game_state, player):
        """
        Core decision logic during the playing phase.
        """
        resources = get_player_resources(game_state, player)
        target = self.choose_target_node(game_state, player)

        # Handle if target is reached
        result = self._handle_reached_target(resources, target, player)
        if result:
            return result

        # Handle if no target is available
        result = self._handle_no_target(resources, target)
        if result:
            return result

        # Handle resource types and trading
        result = self._handle_resource_types_and_trading(resources)
        if result:
            return result

        # Try to build a road towards the target
        if can_try_road(resources):
            edge = self.pick_road_towards_target(game_state, player, target)
            if edge:
                return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

        return {"command": "end_turn", "kwargs": {}}

    def _handle_reached_target(self, resources, target, player):
        if target and self.reached_target(player, target):
            if can_try_settlement(resources):
                self.current_target = None
                return {
                    "command": "place_settlement",
                    "kwargs": {"position": target},
                }
            if self.missing_settlement_resources(resources):
                trade = self.smart_trade(resources)
                if trade:
                    return {"command": "trade_with_bank", "kwargs": trade}
            return {"command": "end_turn", "kwargs": {}}
        return None

    def _handle_no_target(self, resources, target):
        if not target:
            trade = self.smart_trade(resources)
            if trade:
                return {"command": "trade_with_bank", "kwargs": trade}
            return {"command": "end_turn", "kwargs": {}}
        return None

    def _handle_resource_types_and_trading(self, resources):
        resource_types = {r for r, v in resources.items() if v > 0}
        if len(resource_types) == 3:
            return {"command": "end_turn", "kwargs": {}}
        if len(resource_types) <= 2:
            trade = self.smart_trade(resources)
            if trade:
                return {"command": "trade_with_bank", "kwargs": trade}
        return None

    def pick_setup_target_node(self, game_state, player):
        """
        Choose a nearby secondary node during setup to guide initial expansion.
        """
        if not player.settlements:
            return None

        origin = next(iter(player.settlements))
        best_value = -1
        best_node = None

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])

            if not is_valid_setup_settlement_node(game_state, pos):
                continue

            dist = self.dist(origin, pos)
            if dist < 1.5 or dist > 3.0:
                continue

            score = self.score_node(game_state, pos)
            value = score - dist * 2

            if value > best_value:
                best_value = value
                best_node = pos

        return best_node

    def pick_any_setup_road(self, game_state, player):
        """
        Pick any valid road during setup if no directed option exists.
        """
        edges = edges_touching_network(game_state, player)
        if edges:
            return edges[0]
        return None

    def choose_target_node(self, game_state, player):
        """
        Select or maintain the current expansion target.
        """
        if self.current_target:
            if self._is_current_target_valid(game_state):
                return self.current_target
            self.current_target = None

        best_node, _ = self._find_best_target_node(game_state, player)
        self.current_target = best_node
        return best_node

    def _is_current_target_valid(self, game_state):
        """Check whether the current target is still unoccupied."""
        for node in game_state["board"]["nodes"]:
            if tuple(node["position"]) == self.current_target and node["owner"] is None:
                return True
        return False

    def _find_best_target_node(self, game_state, player):
        """
        Find the best reachable node for expansion.
        """
        best_value = -1
        best_node = None

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])

            if not is_valid_setup_settlement_node(game_state, pos):
                continue

            score = self.score_node(game_state, pos)
            dist = self.distance_to_network(player, pos)

            if dist == 0:
                continue

            value = score / (dist + 0.5)

            if value > best_value:
                best_value = value
                best_node = pos

        return best_node, best_value

    def pick_best_node(self, game_state):
        """Pick the highest scoring valid node."""
        best_score = -1
        best_node = None

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])

            if not is_valid_setup_settlement_node(game_state, pos):
                continue

            score = self.score_node(game_state, pos)

            if score > best_score:
                best_score = score
                best_node = pos

        return best_node

    def score_node(self, game_state, node_pos):
        """Compute a heuristic score for a node."""
        score = 0
        resources = set()

        for tile in game_state["board"]["tiles"]:
            center = (tile["q"], tile["r"])
            if self.dist(center, node_pos) > 1.2:
                continue

            if tile["resource"] == "desert":
                score -= 5
                continue

            resources.add(tile["resource"])
            score += DICE_SCORE.get(tile["number"], 0)

        score += len(resources) * 2
        return score

    def distance_to_network(self, player, node_pos):
        """Compute distance from node to player's network."""
        network = set(player.settlements)
        for a, b in player.roads:
            network.add(a)
            network.add(b)

        if not network:
            return float("inf")

        return min(self.dist(node_pos, n) for n in network)

    def reached_target(self, player, target):
        """Check if the player's network has reached the target."""
        network = set(player.settlements)
        for a, b in player.roads:
            network.add(a)
            network.add(b)

        return any(self.dist(n, target) <= 1.0 for n in network)

    def pick_road_towards_target(self, game_state, player, target_node):
        """Choose the road that best advances toward the target."""
        if target_node is None:
            return None

        candidate_edges = edges_touching_network(game_state, player)
        if not candidate_edges:
            candidate_edges = free_edges(game_state)

        best_edge = None
        best_score = -1

        for a, b in candidate_edges:
            dist_before = self.dist(a, target_node)
            dist_after = min(
                self.dist(a, target_node),
                self.dist(b, target_node),
            )

            progress = dist_before - dist_after
            node_score = max(
                self.score_node(game_state, a),
                self.score_node(game_state, b),
            )

            score = progress * 15 + node_score * 0.5

            if score > best_score:
                best_score = score
                best_edge = (a, b)

        return best_edge

    def missing_settlement_resources(self, resources):
        """Return the list of missing resources for settlement."""
        need = {"wood", "brick", "wheat", "sheep"}
        return [r for r in need if resources.get(r, 0) == 0]

    def smart_trade(self, resources):
        """Determine the best trade to enable settlement construction."""
        missing = self.missing_settlement_resources(resources)
        if not missing:
            return None

        give_candidates = [r for r, v in resources.items() if v >= 3]
        if not give_candidates:
            return None

        give = max(give_candidates, key=lambda r: resources[r])
        receive = missing[0]

        return {"give": give, "receive": receive, "rate": 3}

    @staticmethod
    def dist(a, b):
        """Compute Euclidean distance between two points."""
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
