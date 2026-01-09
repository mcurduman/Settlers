class StrategyAI:
    """
    Base class for AI strategies in Settlers. All AI strategies should inherit from this.
    """

    @staticmethod
    def get_player_resources(game_state, player):
        for p in game_state["players"]:
            if p["name"] == player.name:
                return p["resources"]
        return {}

    @staticmethod
    def can_try_settlement(resources):
        return (
            resources.get("wood", 0) >= 1
            and resources.get("brick", 0) >= 1
            and resources.get("wheat", 0) >= 1
            and resources.get("sheep", 0) >= 1
        )

    @staticmethod
    def can_try_road(resources):
        return resources.get("wood", 0) >= 1 and resources.get("brick", 0) >= 1

    @staticmethod
    def can_try_trade(resources, rate=3):
        return any(v >= rate for v in resources.values())

    def choose_settlement_location(
        self,
        game_state,
        player,
    ):
        raise NotImplementedError(
            "AI strategy must implement choose_settlement_location."
        )
