import pygame

from client.assets.theme.colors import PALETTE
from client.render.coord import world_to_screen
from client.render.render_helpers import (is_valid_settlement_node,
                                          is_valid_setup_settlement_node)

from .board_constants import NODE_RADIUS


def draw_nodes(screen, nodes, phase, board_rect, board, current_player):
    """
    Draws all board nodes (settlement/city spots) for the current game state.
    Delegates to owned/unowned node renderers.
    """
    for node in nodes:
        pos = world_to_screen(node["position"], board_rect)
        if node["owner"] is None:
            _draw_unowned_node(screen, pos, phase, board, node, current_player)
        else:
            _draw_owned_node(screen, pos, node)


def _draw_unowned_node(screen, pos, phase, board, node, current_player):
    """
    Draws a node that is not owned by any player, highlighting valid placements.
    """
    if (
        phase
        in (
            "PlayingMainState",
            "PlayingTradeWithBankState",
            "PlayingRollState",
        )
        or current_player.lower() != "human"
    ):
        return

    if phase == "PlayingPlaceSettlementState":
        if is_valid_settlement_node(board, node, current_player):
            pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS + 4)
            pygame.draw.circle(screen, (255, 255, 255), pos, NODE_RADIUS + 6, 2)
        else:
            pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)

    elif phase == "SetupPlaceSettlementState":
        if is_valid_setup_settlement_node(board, tuple(node["position"])):
            pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)
            pygame.draw.circle(screen, (255, 255, 255), pos, NODE_RADIUS + 3, 3)
        else:
            pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)

    else:
        pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)


def _draw_owned_node(screen, pos, node):
    """
    Draws a node that is owned by a player, colored by owner type.
    """
    if str(node["owner"]).lower() == "ai":
        pygame.draw.circle(screen, PALETTE["ai"], pos, NODE_RADIUS)
    else:
        pygame.draw.circle(screen, PALETTE["human"], pos, NODE_RADIUS)
