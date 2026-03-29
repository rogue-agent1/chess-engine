from chess_engine import Board, algebraic, from_algebraic
b = Board()
assert b.grid[7][4] == "K"  # white king
assert b.grid[0][4] == "k"  # black king
moves = b.all_moves()
assert len(moves) == 20  # standard opening: 16 pawn + 4 knight
assert algebraic(7, 4) == "e1"
assert from_algebraic("e1") == (7, 4)
print("Chess engine tests passed")