import math

from engine.game.strategies.ai_helper import edges_touching_network, free_edges
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
    def __init__(self):
        """
        Initializes the Hard AI strategy with internal setup memory.
        """
        self.setup_first_settlement = None

    def choose_action(self, game_state, player):
        """
        Decides the next action for the AI based on the current game state.
        """
        state = game_state["state"]

        if state in ("SetupRollState", "PlayingRollState"):
            return {"command": "roll_dice", "kwargs": {}}

        if state == "SetupPlaceSettlementState":
            if self.setup_first_settlement is None:
                node = self.pick_best_node(game_state)
                self.setup_first_settlement = node
            else:
                node = self.pick_complementary_node(
                    game_state, self.setup_first_settlement
                )

            return {"command": "place_settlement", "kwargs": {"position": node}}

        if state in ("SetupPlaceRoadState", "PlayingPlaceRoadState"):
            target = self.choose_target_node(game_state)
            edge = self.pick_road_towards_target(game_state, player, target)
            return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

        if state == "PlayingMainState":
            resources = StrategyAI.get_player_resources(game_state, player)
            target = self.choose_target_node(game_state)

            if StrategyAI.can_try_settlement(resources):
                return {
                    "command": "place_settlement",
                    "kwargs": {"position": target},
                }

            if StrategyAI.can_try_road(resources):
                edge = self.pick_road_towards_target(game_state, player, target)
                return {
                    "command": "place_road",
                    "kwargs": {"a": edge[0], "b": edge[1]},
                }

            trade = self.smart_trade(resources)
            if trade:
                return {"command": "trade_with_bank", "kwargs": trade}

            return {"command": "end_turn", "kwargs": {}}

        return {"command": "end_turn", "kwargs": {}}

    def pick_best_node(self, game_state):
        """
        Selects the highest scoring available node for settlement placement.
        """
        best_score = -1
        best_node = None

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])
            score = self.score_node(game_state, pos)

            if score > best_score:
                best_score = score
                best_node = pos

        return best_node

    def pick_complementary_node(self, game_state, first_node):
        """
        Selects a node that best complements the resources of the first setup settlement.
        """
        best_score = -1
        best_node = None

        first_resources = self.resources_for_node(game_state, first_node)

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])
            score = self.score_node(game_state, pos)

            resources = self.resources_for_node(game_state, pos)
            missing = resources - first_resources
            score += len(missing) * 4

            if score > best_score:
                best_score = score
                best_node = pos

        return best_node

    def score_node(self, game_state, node_pos):
        """
        Computes a heuristic score for a node based on dice probability and resource diversity.
        """
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

    def resources_for_node(self, game_state, node_pos):
        """
        Returns the set of resources adjacent to a given node.
        """
        res = set()
        for tile in game_state["board"]["tiles"]:
            center = (tile["q"], tile["r"])
            if self.dist(center, node_pos) <= 1.2:
                if tile["resource"] and tile["resource"] != "desert":
                    res.add(tile["resource"])
        return res

    def choose_target_node(self, game_state):
        """
        Chooses the current best target node for expansion.
        """
        return self.pick_best_node(game_state)

    def pick_road_towards_target(self, game_state, player, target_node):
        """
        Selects a road that best advances the player toward the target node.
        """
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

            score = progress * 10 + node_score

            if score > best_score:
                best_score = score
                best_edge = (a, b)

        return best_edge

    def smart_trade(self, resources):
        """
        Determines a trade with the bank that helps enable settlement construction.
        """
        need = {"wood": 1, "brick": 1, "wheat": 1, "sheep": 1}

        missing = [r for r, v in need.items() if resources.get(r, 0) == 0]
        if not missing:
            return None

        give_candidates = [r for r, v in resources.items() if v >= 3]
        if not give_candidates:
            return None

        give = max(give_candidates, key=lambda r: resources[r])
        receive = missing[0]

        return {
            "give": give,
            "receive": receive,
            "rate": 3,
        }

    @staticmethod
    def dist(a, b):
        """
        Computes the Euclidean distance between two points.
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
