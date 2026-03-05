from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MoveCreate(BaseModel):
    x: int
    y: int


class MoveItem(BaseModel):
    player: str
    x: int
    y: int
    created_at: datetime
    board: List[str]       
    raw: Optional[List[List[str]]] = None


class MovesResponse(BaseModel):
    status: str
    winner: Optional[str]
    moves: List[MoveItem] 


class GameResponse(BaseModel):
    id: int
    status: str
    winner: Optional[str]
    created_at: datetime
    finished_at: Optional[datetime]
    board: Optional[List[str]]
    

    class Config:
        from_attributes = True
