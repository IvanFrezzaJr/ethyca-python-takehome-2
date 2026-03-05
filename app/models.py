from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class GameStatus(str):
    PENDING = "pending"
    FINISHED = "finished"


class Player(str):
    X = "X"
    O = "O"


@table_registry.mapped_as_dataclass
class Game:
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[str] = mapped_column(default=GameStatus.PENDING)
    winner: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    moves: Mapped[List["Move"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )


@table_registry.mapped_as_dataclass
class Move:
    __tablename__ = "moves"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player: Mapped[str]
    x: Mapped[int]
    y: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )

    game: Mapped[Game] = relationship(
        back_populates="moves",
        init=False,
    )