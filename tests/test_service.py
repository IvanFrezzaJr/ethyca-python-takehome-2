import pytest
from app.services import TicTacToeService


@pytest.fixture
def service(session):
    return TicTacToeService(session)


def test_create_game(service):
    result = service.create_game()

    assert "id" in result
    assert result["status"] == "pending"
    assert result["winner"] is None
    assert isinstance(result["board"], list)
    assert all(isinstance(row, str) for row in result["board"])


def test_list_games(service):
    _ = service.create_game()
    _ = service.create_game()

    games = service.list_games()
    assert len(games) >= 2

    for game in games:
        assert "board" in game
        assert "raw" in game
        assert isinstance(game["board"], list)
        assert isinstance(game["raw"], list)


def test_make_move_player_and_computer(service):
    game = service.create_game()
    game_id = game["id"]

    result = service.make_move(game_id, 0, 0)
    assert "board" in result
    assert result["status"] in ["pending", "finished"]
    assert result["winner"] in [None, "X", "O", "draw"]

    assert any("X" in row for row in result["board"]) or any("O" in row for row in result["board"])


def test_get_moves_incremental(service):
    game = service.create_game()
    game_id = game["id"]

    result = service.get_moves(game_id)
    assert result["moves"] == []

    service.make_move(game_id, 0, 0)
    service.make_move(game_id, 1, 1)

    result = service.get_moves(game_id)
    assert len(result["moves"]) >= 2
    for move in result["moves"]:
        assert "player" in move
        assert "x" in move
        assert "y" in move
        assert "created_at" in move
        assert "board" in move

        assert "raw" not in move


def test_get_moves_with_raw(service):
    game = service.create_game()
    game_id = game["id"]

    service.make_move(game_id, 0, 0)
    result = service.get_moves(game_id, raw=True)

    for move in result["moves"]:
        assert "raw" in move
        assert isinstance(move["raw"], list)
        assert all(isinstance(row, list) for row in move["raw"])