#!/usr/bin/env python3
"""Simple chess engine with move generation and evaluation."""
import sys

PIECES = {"K":6,"Q":5,"R":4,"B":3,"N":2,"P":1,"k":-6,"q":-5,"r":-4,"b":-3,"n":-2,"p":-1,".":0}
VALUES = {1:100,2:320,3:330,4:500,5:900,6:20000}

class Board:
    def __init__(self):
        self.board = [0]*64; self.turn = 1  # 1=white, -1=black
        setup = "RNBQKBNR"+"P"*8+"."*32+"p"*8+"rnbqkbnr"
        for i,c in enumerate(setup): self.board[i] = PIECES[c]
    def at(self, r, c):
        if 0<=r<8 and 0<=c<8: return self.board[r*8+c]
        return None
    def display(self):
        for r in range(8):
            row = ""
            for c in range(8):
                v = self.board[r*8+c]
                for ch, val in PIECES.items():
                    if val == v and ch != ".": row += ch; break
                else: row += "."
            print(f"  {8-r} {row}")
        print("    abcdefgh")
    def evaluate(self):
        score = 0
        for v in self.board:
            if v > 0: score += VALUES.get(v, 0)
            elif v < 0: score -= VALUES.get(-v, 0)
        return score
    def gen_moves(self):
        moves = []
        for pos in range(64):
            p = self.board[pos]
            if (self.turn == 1 and p > 0) or (self.turn == -1 and p < 0):
                r, c = pos//8, pos%8; ap = abs(p)
                if ap == 1:  # pawn
                    d = -1 if p > 0 else 1
                    if self.at(r+d,c) == 0: moves.append((pos,(r+d)*8+c))
                elif ap == 2:  # knight
                    for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                        nr,nc = r+dr,c+dc
                        if 0<=nr<8 and 0<=nc<8:
                            t = self.at(nr,nc)
                            if t is not None and (t==0 or (t>0)!=(p>0)):
                                moves.append((pos,nr*8+nc))
                elif ap in (4,5,6,3):  # sliding pieces
                    dirs = []
                    if ap in (4,5,6): dirs += [(0,1),(0,-1),(1,0),(-1,0)]
                    if ap in (3,5,6): dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
                    for dr,dc in dirs:
                        nr,nc = r+dr,c+dc
                        while 0<=nr<8 and 0<=nc<8:
                            t = self.at(nr,nc)
                            if t == 0: moves.append((pos,nr*8+nc))
                            elif (t>0)!=(p>0): moves.append((pos,nr*8+nc)); break
                            else: break
                            if ap == 6: break  # king moves 1
                            nr += dr; nc += dc
        return moves

def main():
    b = Board(); b.display()
    moves = b.gen_moves()
    print(f"White moves: {len(moves)}")
    print(f"Eval: {b.evaluate()}")

if __name__ == "__main__": main()
