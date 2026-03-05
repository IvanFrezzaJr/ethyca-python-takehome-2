from typing import Annotated

from app.services import TicTacToeService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas import (
    GameResponse,
    MoveCreate,
    MovesResponse
)

router = APIRouter(prefix="/games", tags=["games"])

T_Session = Annotated[Session, Depends(get_session)]



@router.post("/", response_model=GameResponse, status_code=201)
def create_game(session: T_Session):
    service = TicTacToeService(session)
    return service.create_game()


@router.get("/", response_model=list[GameResponse])
def list_games(session: T_Session):
    service = TicTacToeService(session)
    return service.list_games()


@router.post("/{game_id}/moves")
def make_move(game_id: int, move: MoveCreate, session: T_Session, raw: bool = Query(False)):
    service = TicTacToeService(session)
    return service.make_move(game_id, move.x, move.y, raw=raw)


@router.get("/{game_id}/moves", response_model=MovesResponse)
def list_moves(game_id: int, session: T_Session, raw: bool = False):
    service = TicTacToeService(session)
    return service.get_moves(game_id, raw=raw)