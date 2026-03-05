import random
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import GameRepository, MoveRepository


class TicTacToeService:
    BOARD_SIZE = 3

    def __init__(self, db: Session):
        self.game_repo = GameRepository(db)
        self.move_repo = MoveRepository(db)

    def create_game(self):
        game = self.game_repo.create()

        board_state = [["." for _ in range(3)] for _ in range(3)]
        
        return {
            "id": game.id,
            "status": game.status,
            "winner": game.winner,
            "created_at": game.created_at,
            "finished_at": game.finished_at,
            "board": self._ascii_board(board_state),
        }

    def list_games(self):
        games = self.game_repo.list()
        result = []

        for game in games:

            board_state = self._build_board(game.id)  
            result.append({
                "id": game.id,
                "status": game.status,
                "winner": game.winner,
                "created_at": game.created_at,
                "finished_at": game.finished_at,
                "board": self._ascii_board(board_state),  
                "raw": board_state,                      
            })

        return result

    def get_moves(self, game_id: int, raw: bool = False):
        game = self._get_game_or_404(game_id)
        moves = self.move_repo.list_by_game(game.id)

        board_state = [["." for _ in range(3)] for _ in range(3)]
        moves_list = []

        for move in moves:
            board_state[move.x][move.y] = move.player

            moves_list.append({
                "player": move.player,
                "x": move.x,
                "y": move.y,
                "created_at": move.created_at,
                "board": self._ascii_board(board_state),
                **({"raw": [row.copy() for row in board_state]} if raw else {})
            })

        return {
            "status": game.status,
            "winner": game.winner,
            "moves": moves_list
        }

    def make_move(self, game_id: int, x: int, y: int, raw: bool = False):
        game = self._get_game_or_404(game_id)

        if game.status == "finished":
            raise HTTPException(status_code=409, detail="Game already finished.")

        if not self._is_valid_position(x, y):
            raise HTTPException(status_code=400, detail="Invalid position.")

        board_state = self._build_board(game.id)

        if board_state[x][y] != ".":
            raise HTTPException(status_code=409, detail="Position already taken.")

        self.move_repo.create(game.id, "X", x, y)
        board_state[x][y] = "X"

        if self._check_winner(board_state, "X"):
            return self._finish_game(game, "X", board_state, raw)

        if self._is_draw(board_state):
            return self._finish_game(game, "draw", board_state, raw)

        empty_cells = [(i, j) for i in range(3) for j in range(3) if board_state[i][j] == "."]
        comp_x, comp_y = random.choice(empty_cells)
        self.move_repo.create(game.id, "O", comp_x, comp_y)
        board_state[comp_x][comp_y] = "O"

        if self._check_winner(board_state, "O"):
            return self._finish_game(game, "O", board_state, raw)

        if self._is_draw(board_state):
            return self._finish_game(game, "draw", board_state, raw)

        return {
            "status": game.status,
            "winner": game.winner,
            "board": self._ascii_board(board_state),
            **({"raw": board_state} if raw else {}),
        }


    def _get_game_or_404(self, game_id: int):
        game = self.game_repo.get(game_id)
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found.",
            )
        return game
        
    def _ascii_board(self, board_state: list[list[str]]) -> list[str]:
        return ["  " + "  |  ".join(row) + "  " for row in board_state]

    def _build_board(self, game_id: int):
        board = [["." for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        moves = self.move_repo.list_by_game(game_id)
        for move in moves:
            board[move.x][move.y] = move.player
        return board

    def _check_winner(self, board, player: str):
        lines = []

        lines.extend(board)  # rows
        lines.extend([[board[i][j] for i in range(3)] for j in range(3)])  # columns
        lines.append([board[i][i] for i in range(3)])  # diagonal
        lines.append([board[i][2 - i] for i in range(3)])  # anti-diagonal

        return any(all(cell == player for cell in line) for line in lines)

    def _is_draw(self, board):
        return all(cell != "." for row in board for cell in row)

    def _is_valid_position(self, x: int, y: int):
        return 0 <= x < 3 and 0 <= y < 3

    def _finish_game(self, game, winner: str, board_state: list[list[str]], raw: bool):
        game.status = "finished"
        game.winner = winner
        game.finished_at = datetime.now(timezone.utc)
        self.game_repo.save(game)

        return {
            "status": game.status,
            "winner": game.winner,
            "board": self._ascii_board(board_state),
            **({"raw": board_state} if raw else {}),
        }