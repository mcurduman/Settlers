import math

from engine.game.strategies.ai_helper import (can_try_road, can_try_settlement,
                                              edges_touching_network,
                                              get_player_resources,
                                              is_valid_settlement_node,
                                              is_valid_setup_settlement_node)
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
    Hard AI strategy with explicit planning.

    Key ideas:
    - TARGET is an expansion intention, not a build condition.
    - ROAD phase continues until there is any real settlement opportunity.
    - SETTLEMENT phase triggers as soon as a legal settlement is possible
      anywhere in the current road network.
    """

    def __init__(self):
        """
        Initialize the Hard AI strategy with current target and build phase.
        """
        self.current_target = None
        self.build_phase = "road"

    def choose_action(self, game_state, player):
        """
        Decide what action the AI should take based on game state and resources.
        """
        state = game_state["state"]

        if state in ("SetupRollState", "PlayingRollState"):
            return {"command": "roll_dice", "kwargs": {}}

        if state == "SetupPlaceSettlementState":
            node = self.pick_best_node(game_state)
            return {"command": "place_settlement", "kwargs": {"position": node}}

        if state == "SetupPlaceRoadState":
            edges = edges_touching_network(game_state, player)
            if edges:
                a, b = edges[0]
                return {"command": "place_road", "kwargs": {"a": a, "b": b}}
            return {"command": "end_turn", "kwargs": {}}

        if state == "PlayingMainState":
            return self._play_main(game_state, player)

        if state == "PlayingPlaceRoadState":
            target = self.choose_target_node(game_state, player)
            if not target:
                return {"command": "end_turn", "kwargs": {}}

            edge = self.pick_road_towards_target(game_state, player, target)
            if not edge:
                return {"command": "end_turn", "kwargs": {}}

            return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

        return {"command": "end_turn", "kwargs": {}}

    def _play_main(self, game_state, player):
        """
        Main logic for the AI's playing phase.
        Decides whether to build a road, settlement, or trade.
        """
        board = game_state["board"]
        resources = get_player_resources(game_state, player)

        # Print current resources for debugging
        print(f"[AI] Resources = {resources}")

        # If a settlement can be built immediately, do it
        if can_try_settlement(resources):
            immediate = self.find_best_immediate_settlement(board, player)
            if immediate:
                print(f"[AI] Immediate settlement at {immediate}")
                self.current_target = None
                self.build_phase = "road"
                return {
                    "command": "place_settlement",
                    "kwargs": {"position": immediate},
                }

        target = self.choose_target_node(game_state, player)
        print(f"[AI] Current target = {target}")

        if not target:
            print("[AI] No expansion target available")
            return {"command": "end_turn", "kwargs": {}}

        # Decide build phase based on available opportunities
        if self.has_any_valid_settlement(board, player):
            self.build_phase = "settlement"
        else:
            self.build_phase = "road"

        print(f"[AI] Build phase = {self.build_phase}")

        # If in road phase, try to build a road or trade for road resources
        if self.build_phase == "road":
            if can_try_road(resources):
                edge = self.pick_road_towards_target(game_state, player, target)
                if edge:
                    print(f"[AI] Placing road {edge}")
                    return {
                        "command": "place_road",
                        "kwargs": {"a": edge[0], "b": edge[1]},
                    }

            trade = self.smart_trade(resources, intent="road")
            if trade:
                print(f"[AI] Trading for road: {trade}")
                return {"command": "trade_with_bank", "kwargs": trade}

            return {"command": "end_turn", "kwargs": {}}

        # If in settlement phase, try to build a settlement or trade for settlement resources
        node_obj = self._get_node_by_pos(board, target)
        if node_obj and can_try_settlement(resources):
            if is_valid_settlement_node(board, node_obj, player.name):
                print(f"[AI] Settlement at target {target}")
                self.current_target = None
                self.build_phase = "road"
                return {
                    "command": "place_settlement",
                    "kwargs": {"position": target},
                }

        trade = self.smart_trade(resources, intent="settlement")
        if trade:
            print(f"[AI] Trading for settlement: {trade}")
            return {"command": "trade_with_bank", "kwargs": trade}

        return {"command": "end_turn", "kwargs": {}}

    def has_any_valid_settlement(self, board, player):
        """
        Checks if the player can build a settlement on any node in the current road network.
        """
        for node in board["nodes"]:
            if is_valid_settlement_node(board, node, player.name):
                return True
        return False

    def find_best_immediate_settlement(self, board, player):
        """
        Chooses the best settlement that can be built immediately, ignoring long-term plans.
        """
        best_score = -1
        best_pos = None

        for node in board["nodes"]:
            pos = tuple(node["position"])
            if is_valid_settlement_node(board, node, player.name):
                # Calculate score for each valid node
                score = self.score_node({"board": board}, pos)
                if score > best_score:
                    best_score = score
                    best_pos = pos

        return best_pos

    def choose_target_node(self, game_state, player):
        """
        Selects or maintains the AI's expansion target.
        """
        if self.current_target:
            if self.is_valid_target_node(game_state, self.current_target, player):
                return self.current_target
            self.current_target = None

        best_node, _ = self._find_best_target_node(game_state, player)
        if best_node and self.is_valid_target_node(game_state, best_node, player):
            self.current_target = best_node
            return best_node

        return None

    def is_valid_target_node(self, game_state, node_pos, player):
        """
        Checks if a node can be a valid expansion target.
        """
        board = game_state["board"]

        for n in board["nodes"]:
            if tuple(n["position"]) == node_pos and n["owner"] is not None:
                return False

        if not is_valid_setup_settlement_node(game_state, node_pos):
            return False

        # The node must not already be in the player's network
        network = set(player.settlements)
        for a, b in player.roads:
            network.add(a)
            network.add(b)

        return node_pos not in network

    def _find_best_target_node(self, game_state, player):
        """
        Finds the best node for the AI to expand towards.
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

    def pick_road_towards_target(self, game_state, player, target):
        """
        Picks the road that brings the player closest to the target.
        """
        edges = edges_touching_network(game_state, player)
        if not edges:
            return None

        best_edge = None
        best_score = -1

        for a, b in edges:
            # Calculate progress towards target if this road is built
            before = self.dist(a, target)
            after = min(self.dist(a, target), self.dist(b, target))
            score = before - after

            if score > best_score:
                best_score = score
                best_edge = (a, b)

        return best_edge

    def score_node(self, game_state, pos):
        """
        Calculates the score of a node based on surrounding resources and dice numbers.
        """
        score = 0
        for tile in game_state["board"]["tiles"]:
            center = (tile["q"], tile["r"])
            # If the node is near a resource (not desert), add the dice score
            if self.dist(center, pos) <= 1.2 and tile["resource"] != "desert":
                score += DICE_SCORE.get(tile["number"], 0)
        return score

    def smart_trade(self, resources, intent):
        """
        Decides what trade the AI should make based on intent (road or settlement).
        """
        if intent == "road":
            need = {"wood", "brick"}
        else:
            need = {"wood", "brick", "wheat", "sheep"}

        # What resources are missing for the current intent
        missing = [r for r in need if resources.get(r, 0) == 0]
        if not missing:
            return None

        # What resources can be given to the bank (if we have >=3 of a type)
        give_candidates = [r for r, v in resources.items() if v >= 3]
        if not give_candidates:
            return None

        return {"give": give_candidates[0], "receive": missing[0], "rate": 3}

    def pick_best_node(self, game_state):
        """
        Picks the best free node for settlement during setup.
        """
        best_score = -1
        best_node = None
        for node in game_state["board"]["nodes"]:
            if node["owner"] is None:
                pos = tuple(node["position"])
                if is_valid_setup_settlement_node(game_state, pos):
                    score = self.score_node(game_state, pos)
                    if score > best_score:
                        best_score = score
                        best_node = pos
        return best_node

    def distance_to_network(self, player, pos):
        """
        Calculates the minimum distance from a node to the player's network.
        """
        network = set(player.settlements)
        for a, b in player.roads:
            network.add(a)
            network.add(b)
        return min(self.dist(pos, n) for n in network) if network else float("inf")

    @staticmethod
    def _get_node_by_pos(board, pos):
        """
        Returns the node object with the given position from the board.
        """
        for n in board["nodes"]:
            if tuple(n["position"]) == pos:
                return n
        return None

    @staticmethod
    def dist(a, b):
        """
        Calculates the Euclidean distance between two positions.
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
