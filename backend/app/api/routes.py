from fastapi import APIRouter, HTTPException
from app.services.game_service import GameService

router = APIRouter(prefix="/game", tags=["game"])

game_service = GameService()


# -------------------------------------------------
# Game lifecycle
# -------------------------------------------------
@router.post("/start")
def start_game(difficulty: str):
    try:
        return game_service.start_game(difficulty)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/state")
def get_state():
    try:
        return game_service.get_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------
# Commands
# -------------------------------------------------
@router.post("/roll-dice")
def roll_dice():
    try:
        return game_service.roll_dice()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trade")
def trade_with_bank(give: str, receive: str):
    try:
        return game_service.trade_with_bank(give, receive)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/place-settlement")
def place_settlement(position: int):
    try:
        return game_service.place_settlement(position)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
