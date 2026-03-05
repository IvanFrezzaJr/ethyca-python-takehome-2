from sqlalchemy.orm import Session

from app.models import Game, Move


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self) -> Game:
        game = Game()
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get(self, game_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def list(self) -> list[Game]:
        return self.db.query(Game).order_by(Game.created_at).all()

    def save(self, game: Game) -> None:
        self.db.commit()
        self.db.refresh(game)


class MoveRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, game_id: int, player: str, x: int, y: int) -> Move:
        move = Move(game_id=game_id, player=player, x=x, y=y)
        self.db.add(move)
        self.db.commit()
        self.db.refresh(move)
        return move

    def list_by_game(self, game_id: int) -> list[Move]:
        return (
            self.db.query(Move)
            .filter(Move.game_id == game_id)
            .order_by(Move.created_at)
            .all()
        )