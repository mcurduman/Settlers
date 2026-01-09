def _describe_place_road(board, kwargs):
    """
    Returns a human-friendly description for a road placement action.
    """
    a = tuple(kwargs.get("a"))
    b = tuple(kwargs.get("b"))
    tile_numbers = set()
    for tile in board.tiles:
        corners = [tuple(round(x, 2) for x in c) for c in tile.corners(board.size)]
        if (a in corners or b in corners) and tile.number is not None:
            tile_numbers.add(tile.number)
    if tile_numbers:
        return f"AI placed a road near tile(s) {sorted(tile_numbers)}"
    return f"AI placed a road between {a} and {b}"


def _describe_place_settlement(board, kwargs):
    """
    Returns a human-friendly description for a settlement placement action.
    """
    pos = tuple(kwargs.get("position"))
    tile_numbers = []
    for tile in board.tiles:
        corners = [tuple(round(x, 2) for x in c) for c in tile.corners(board.size)]
        if pos in corners and tile.number is not None:
            tile_numbers.append(tile.number)
    if tile_numbers:
        return f"AI placed a settlement near tile(s) {sorted(tile_numbers)}"
    return f"AI placed a settlement at {pos}"


def _describe_roll_dice(board, kwargs):
    """
    Returns a human-friendly description for a dice roll action.
    """
    return "AI rolled the dice"


def _describe_trade_with_bank(board, kwargs):
    """
    Returns a human-friendly description for a trade with the bank action.
    """
    give = kwargs.get("give")
    receive = kwargs.get("receive")
    rate = kwargs.get("rate", 3)
    return f"AI traded {rate} {give} for 1 {receive} at the bank"


def _describe_end_turn(board, kwargs):
    """
    Returns a human-friendly description for an end turn action.
    """
    return "AI ended its turn"


def describe_ai_action(game, command_name, kwargs):
    """
    Returns a human-friendly description for an AI action.
    """
    board = game.board
    handlers = {
        "place_road": _describe_place_road,
        "place_settlement": _describe_place_settlement,
        "roll_dice": _describe_roll_dice,
        "trade_with_bank": _describe_trade_with_bank,
        "end_turn": _describe_end_turn,
    }
    handler = handlers.get(command_name)
    if handler:
        return handler(board, kwargs)
    return f"AI executed {command_name} with {kwargs}"
