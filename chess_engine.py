#!/usr/bin/env python3
"""Simple chess engine with move generation. Zero dependencies."""
import sys

PIECES = {"K": "king", "Q": "queen", "R": "rook", "B": "bishop", "N": "knight", "P": "pawn"}

class Board:
    def __init__(self):
        self.grid = [["." for _ in range(8)] for _ in range(8)]
        self.turn = "w"
        self.castling = "KQkq"
        self.setup()

    def setup(self):
        order = ["R","N","B","Q","K","B","N","R"]
        for i in range(8):
            self.grid[0][i] = order[i].lower()
            self.grid[1][i] = "p"
            self.grid[6][i] = "P"
            self.grid[7][i] = order[i]

    def at(self, r, c):
        if 0<=r<8 and 0<=c<8: return self.grid[r][c]
        return None

    def is_white(self, piece): return piece.isupper()
    def is_black(self, piece): return piece.islower() and piece != "."

    def moves_for(self, r, c):
        p = self.grid[r][c]
        if p == ".": return []
        white = p.isupper()
        moves = []
        pt = p.upper()
        if pt == "P":
            d = -1 if white else 1
            if self.at(r+d,c) == ".":
                moves.append((r+d,c))
                start = 6 if white else 1
                if r == start and self.at(r+2*d,c) == ".":
                    moves.append((r+2*d,c))
            for dc in (-1,1):
                t = self.at(r+d,c+dc)
                if t and t != "." and self.is_white(t) != white:
                    moves.append((r+d,c+dc))
        elif pt == "N":
            for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                nr,nc=r+dr,c+dc
                t = self.at(nr,nc)
                if t is not None and (t=="." or self.is_white(t)!=white):
                    moves.append((nr,nc))
        elif pt in "RBQ":
            dirs = []
            if pt in "RQ": dirs += [(0,1),(0,-1),(1,0),(-1,0)]
            if pt in "BQ": dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr,dc in dirs:
                nr,nc = r+dr,c+dc
                while self.at(nr,nc) is not None:
                    if self.at(nr,nc) == ".":
                        moves.append((nr,nc))
                    elif self.is_white(self.at(nr,nc)) != white:
                        moves.append((nr,nc)); break
                    else: break
                    nr+=dr; nc+=dc
        elif pt == "K":
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    t=self.at(r+dr,c+dc)
                    if t is not None and (t=="." or self.is_white(t)!=white):
                        moves.append((r+dr,c+dc))
        return moves

    def all_moves(self):
        white = self.turn == "w"
        result = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p != "." and p.isupper() == white:
                    for mr,mc in self.moves_for(r,c):
                        result.append((r,c,mr,mc))
        return result

    def make_move(self, r1,c1,r2,c2):
        self.grid[r2][c2] = self.grid[r1][c1]
        self.grid[r1][c1] = "."
        self.turn = "b" if self.turn == "w" else "w"

    def to_fen_board(self):
        rows = []
        for r in range(8):
            empty = 0; row = ""
            for c in range(8):
                if self.grid[r][c] == ".": empty += 1
                else:
                    if empty: row += str(empty); empty = 0
                    row += self.grid[r][c]
            if empty: row += str(empty)
            rows.append(row)
        return "/".join(rows)

    def display(self):
        lines = ["  a b c d e f g h"]
        for r in range(8):
            row = f"{8-r} " + " ".join(self.grid[r])
            lines.append(row)
        return "\n".join(lines)

def algebraic(r, c): return chr(ord("a")+c) + str(8-r)
def from_algebraic(s): return 8-int(s[1]), ord(s[0])-ord("a")

if __name__ == "__main__":
    b = Board()
    print(b.display())
    moves = b.all_moves()
    print(f"\n{len(moves)} legal moves for {'white' if b.turn=='w' else 'black'}")
