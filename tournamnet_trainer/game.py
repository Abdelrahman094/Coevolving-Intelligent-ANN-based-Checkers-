from constants import RED, WHITE,GREY,BLACK, BLUE, SQUARE_SIZE
from board import Board
from piece import Piece

class Move:
    def __init__(self, piece: Piece, to_position: tuple, skipped: Piece = None):
        self.from_position = (piece.row, piece.col)
        self.to_position = to_position
        self.skipped = skipped




class AI_Game:
    def __init__(self, network=None):
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.selected = None
        self.network = network

    def update(self):
        pass  # Remove pygame-related code

    def reset(self):
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.selected = None

    def winner(self):
        return self.board.winner()

    def select(self, row: int, col: int) -> bool:
        if self.selected:
            if self._move(row, col):
                return True
            self.selected = None
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row: int, col: int) -> bool:
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == BLACK else BLACK

    def get_board(self):
        return self.board

    def get_game_state(self):
        return {
            'board': self.board,
            'turn': self.turn,
            'valid_moves': self.valid_moves,
            'selected': self.selected
        }

    def get_fen(self):
        fen = ""
        empty_count = 0
        for row in self.board.board:
            for piece in row:
                if piece is None:
                    empty_count += 1
                elif piece.color == BLACK:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += "r"
                elif piece.color == WHITE:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += "w"
                else:
                    fen += str(empty_count)
                    empty_count = 0
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            if not all(p is not None for p in row):
                fen += "/"
        fen += " " + self.turn
        return fen

    def get_move(self, game_state):
        board = Board.from_dict(game_state['board'])
        turn = game_state['turn']
        valid_moves = game_state['valid_moves']
        selected = game_state['selected']

        moves = self.get_moves(board, turn, valid_moves, selected)

        best_move = None
        best_value = float('-inf')

        for move in moves:
            new_board = Board.from_dict(board.to_dict())
            new_board.Move(move.from_position, move.to_position)

            value = self.network.predict(new_board.to_dict())

            if value > best_value:
                best_move = move
                best_value = value

        return f"{best_move.from_position}-{best_move.to_position}"

    def get_moves(self, board: Board, turn: str, valid_moves: dict, selected: Piece) -> list:
        moves = []
        for move, skipped in valid_moves.items():
            if skipped:
                moves.append(Move(selected, move, skipped))
            else:
                moves.append(Move(selected, move))
        return moves



















# class Game:
#     def __init__(self) -> None:
#         self.board = Board()
#         self.turn = RED
#         self.valid_moves = {}
#         self.selected = None

#     def update(self) -> None:
#         pass  # Remove pygame-related code

#     def reset(self) -> None:
#         self.board = Board()
#         self.turn = RED
#         self.valid_moves = {}
#         self.selected = None

#     def winner(self) -> str:
#         return self.board.winner()

#     def select(self, row: int, col: int) -> bool:
#         if self.selected:
#             if self._move(row, col):
#                 return True
#             self.selected = None
#         piece = self.board.get_piece(row, col)
#         if piece and piece.color == self.turn:
#             self.selected = piece
#             self.valid_moves = self.board.get_valid_moves(piece)
#             return True
#         return False

#     def _move(self, row: int, col: int) -> bool:
#         piece = self.board.get_piece(row, col)
#         if self.selected and piece == 0 and (row, col) in self.valid_moves:
#             self.board.move(self.selected, row, col)
#             skipped = self.valid_moves[(row, col)]
#             if skipped:
#                 self.board.remove(skipped)
#             self.change_turn()
#             return True
#         return False

#     def change_turn(self) -> None:
#         self.valid_moves = {}
#         self.turn = WHITE if self.turn == RED else RED

#     def get_board(self) -> Board:
#         return self.board

#     def get_game_state(self) -> dict:
#         return {
#             'board': self.board,
#             'turn': self.turn,
#             'valid_moves': self.valid_moves,
#             'selected': self.selected
#         }
#     def get_fen(self) -> str:
#         fen = ""
#         empty_count = 0
#         for row in self.board.board:
#             for piece in row:
#                 if piece is None:
#                     empty_count += 1
#                 elif piece.color == RED:
#                     if empty_count > 0:
#                         fen += str(empty_count)
#                         empty_count = 0
#                     fen += "r"
#                 elif piece.color == WHITE:
#                     if empty_count > 0:
#                         fen += str(empty_count)
#                         empty_count = 0
#                     fen += "w"
#                 else:
#                     fen += str(empty_count)
#                     empty_count = 0
#             if empty_count > 0:
#                 fen += str(empty_count)
#                 empty_count = 0
#             if not all(p is not None for p in row):
#                 fen += "/"
#         fen += " " + self.turn
#         return fen
    
# class AI:
#     def __init__(self, network):
#         self.network = network

#     def get_move(self, game_state: dict) -> str:
#         board = Board.from_dict(game_state['board'])
#         turn = game_state['turn']
#         valid_moves = game_state['valid_moves']
#         selected = game_state['selected']

#         moves = self.get_moves(board, turn, valid_moves, selected)

#         best_move = None
#         best_value = float('-inf')

#         for move in moves:
#             new_board = Board.from_dict(board.to_dict())
#             new_board.move(move.from_position, move.to_position)

#             value = self.network.predict(new_board.to_dict())

#             if value > best_value:
#                 best_move = move
#                 best_value = value

#         return f"{best_move.from_position}-{best_move.to_position}"

#     def get_moves(self, board: Board, turn: str, valid_moves: dict, selected: Piece) -> list:
#         moves = []
#         for move, skipped in valid_moves.items():
#             if skipped:
#                 moves.append(Move(selected, move, skipped))
#             else:
#                 moves.append(Move(selected, move))
#         return moves
    
    
