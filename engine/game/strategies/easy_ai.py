import random

from engine.game.strategies.ai_helper import (edges_touching_network,
                                              free_edges,
                                              is_desert_plus_resource)
from engine.game.strategies.strategy_ai import StrategyAI


class EasyAIStrategy(StrategyAI):

    def choose_action(self, game_state, player):
        """
        Decides the next action for the AI based on the current game state.
        """
        state = game_state["state"]

        if state == "SetupPlaceSettlementState":
            return self._action_setup_place_settlement(game_state)

        if state in ("SetupPlaceRoadState", "PlayingPlaceRoadState"):
            return self._action_place_road(game_state, player)

        if state in ("SetupRollState", "PlayingRollState"):
            return self._action_roll_dice()

        if state == "PlayingMainState":
            return self._action_playing_main(game_state, player)

        return {"command": "end_turn", "kwargs": {}}

    def _action_setup_place_settlement(self, game_state):
        node = self.pick_bad_but_not_terrible_node(game_state)
        return {"command": "place_settlement", "kwargs": {"position": node}}

    def _action_place_road(self, game_state, player):
        edge = self.pick_random_connected_road(game_state, player)
        return {"command": "place_road", "kwargs": {"a": edge[0], "b": edge[1]}}

    def _action_roll_dice(self):
        return {"command": "roll_dice", "kwargs": {}}

    def _action_playing_main(self, game_state, player):
        resources = StrategyAI.get_player_resources(game_state, player)
        possible_actions = ["end_turn"]

        if StrategyAI.can_try_road(resources):
            possible_actions.append("road")
        if StrategyAI.can_try_settlement(resources):
            possible_actions.append("settlement")
        if StrategyAI.can_try_trade(resources):
            possible_actions.append("trade")

        if not possible_actions:
            return {"command": "end_turn", "kwargs": {}}

        action = random.choice(possible_actions)

        if action == "road":
            return self._action_place_road(game_state, player)
        if action == "settlement":
            return self._action_setup_place_settlement(game_state)
        if action == "trade":
            return self._action_trade_with_bank(resources)

        return {"command": "end_turn", "kwargs": {}}

    def _action_trade_with_bank(self, resources):
        give_candidates = [r for r, v in resources.items() if v >= 3]
        give = random.choice(give_candidates)
        resources_types = ["wood", "brick", "sheep", "wheat"]
        receive_candidates = [
            r for r in resources_types if r != give and resources.get(r, 0) == 0
        ]
        print(f"AI trade candidates: give {give}, receive {resources.items()}")
        if not receive_candidates:
            receive_candidates = [r for r in resources.keys() if r != give]
        receive = random.choice(receive_candidates)

        return {
            "command": "trade_with_bank",
            "kwargs": {
                "give": give,
                "receive": receive,
                "rate": 3,
            },
        }

    def pick_bad_but_not_terrible_node(self, game_state):
        """
        Picks a suboptimal but valid node for settlement placement.
        """
        candidates = []

        for node in game_state["board"]["nodes"]:
            if node["owner"] is not None:
                continue

            pos = tuple(node["position"])

            if is_desert_plus_resource(game_state, pos):
                candidates.append(pos)

        if candidates:
            return random.choice(candidates)

        # fallback: orice nod liber
        free_nodes = [
            tuple(n["position"])
            for n in game_state["board"]["nodes"]
            if n["owner"] is None
        ]
        return random.choice(free_nodes)

    def pick_random_connected_road(self, game_state, player):
        """
        Picks a random road edge connected to the player's network, or any free edge.
        """
        edges = edges_touching_network(game_state, player)

        if edges:
            return random.choice(edges)

        # fallback: orice edge liber
        all_free = free_edges(game_state)
        return random.choice(all_free)
