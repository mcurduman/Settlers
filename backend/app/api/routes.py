from fastapi import APIRouter, HTTPException
from typing import Tuple
from app.services.game_service import GameService

router = APIRouter(prefix="/game")

game_service = GameService()


# Game lifecycle
@router.post("/start", tags=["game"])
def start_game(difficulty: str):
    try:
        return game_service.start_game(difficulty)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/end", tags=["game"])
def end_game():
    try:
        return game_service.end_game()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# End player turn
@router.post("/end-turn", tags=["game"])
def end_turn():
    try:
        return game_service.end_turn()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/state", tags=["game-state"])
def get_state():
    try:
        return game_service.get_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Commands
@router.post("/roll-dice", tags=["commands"])
def roll_dice():
    try:
        return game_service.roll_dice()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trade", tags=["commands"])
def trade_with_bank(give: str, receive: str):
    try:
        return game_service.trade_with_bank(give, receive)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/place-settlement", tags=["commands"])
def place_settlement(position: Tuple[float, float]):
    try:
        return game_service.place_settlement(position)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/place-road", tags=["commands"])
def place_road(a: Tuple[float, float], b: Tuple[float, float]):
    try:
        return game_service.place_road(a, b)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
