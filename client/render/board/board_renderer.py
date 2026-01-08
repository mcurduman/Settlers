from .board_assets import load_tile_icons
from .tile_renderer import draw_tiles
from .edge_renderer import draw_edges
from .node_renderer import draw_nodes


def draw_board(screen, state, board_rect):
    """
    Orchestrates the rendering of the game board.
    Draws tiles, edges, and nodes based on the current game state.

    Args:
        screen: The pygame surface to draw on.
        state: The current game state dictionary.
        board_rect: The rectangle area for the board.
    """
    board = state["board"]
    phase = state.get("state", "")
    current_player = state.get("current_player", "")

    icons = load_tile_icons()

    draw_tiles(screen, board["tiles"], board_rect, icons)
    draw_edges(screen, board["edges"], board, phase, current_player, board_rect)
    draw_nodes(
        screen,
        board["nodes"],
        phase,
        board_rect,
        board,
        current_player,
    )
