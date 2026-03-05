import pytest
from sqlalchemy.orm import Session

from app.models import Game
from app.repositories import GameRepository, MoveRepository


@pytest.fixture
def game_repo(session: Session) -> GameRepository:
    return GameRepository(session)


@pytest.fixture
def move_repo(session: Session) -> MoveRepository:
    return MoveRepository(session)


def test_create_game(game_repo: GameRepository, session: Session):
    game = game_repo.create()
    assert game.id is not None
    assert game.status == "pending"

    db_game = session.query(Game).get(game.id)
    assert db_game is not None


def test_get_game(game_repo: GameRepository):
    game = game_repo.create()
    fetched = game_repo.get(game.id)
    assert fetched is not None
    assert fetched.id == game.id

    assert game_repo.get(9999) is None


def test_list_games(game_repo: GameRepository):

    g1 = game_repo.create()
    g2 = game_repo.create()

    games = game_repo.list()
    assert len(games) >= 2
    assert g1 in games
    assert g2 in games


def test_save_game(game_repo: GameRepository):
    game = game_repo.create()
    game.status = "finished"
    game_repo.save(game)

    db_game = game_repo.get(game.id)
    assert db_game.status == "finished"


def test_create_move(move_repo: MoveRepository, game_repo: GameRepository):
    game = game_repo.create()
    move = move_repo.create(game.id, "X", 1, 1)

    assert move.id is not None
    assert move.player == "X"
    assert move.x == 1
    assert move.y == 1
    assert move.game_id == game.id


def test_list_moves(move_repo: MoveRepository, game_repo: GameRepository):
    game = game_repo.create()

    move1 = move_repo.create(game.id, "X", 0, 0)
    move2 = move_repo.create(game.id, "O", 1, 1)

    moves = move_repo.list_by_game(game.id)
    assert len(moves) == 2
    assert moves[0].id == move1.id
    assert moves[1].id == move2.id

    empty_game = game_repo.create()
    empty_moves = move_repo.list_by_game(empty_game.id)
    assert empty_moves == []