#!/usr/bin/env python3
"""Simple chess engine with move generation and evaluation."""
PIECES="PNBRQKpnbrqk"
INIT_BOARD="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
def parse_fen(fen):
    board=[]
    for row in fen.split("/"):
        r=[]
        for c in row:
            if c.isdigit(): r.extend(["."] * int(c))
            else: r.append(c)
        board.append(r)
    return board
def to_fen(board):
    rows=[]
    for row in board:
        s="";empty=0
        for c in row:
            if c==".": empty+=1
            else:
                if empty: s+=str(empty);empty=0
                s+=c
        if empty: s+=str(empty)
        rows.append(s)
    return "/".join(rows)
def evaluate(board):
    values={"P":1,"N":3,"B":3,"R":5,"Q":9,"K":0,"p":-1,"n":-3,"b":-3,"r":-5,"q":-9,"k":0}
    score=0
    for row in board:
        for c in row:
            if c in values: score+=values[c]
    return score
def gen_moves(board,white=True):
    moves=[]
    for r in range(8):
        for c in range(8):
            p=board[r][c]
            if p=="." or (white and p.islower()) or (not white and p.isupper()): continue
            if p in "Pp":
                d=-1 if p.isupper() else 1
                if 0<=r+d<8 and board[r+d][c]==".": moves.append((r,c,r+d,c))
                for dc in [-1,1]:
                    if 0<=r+d<8 and 0<=c+dc<8:
                        t=board[r+d][c+dc]
                        if t!="." and t.islower()!=p.islower(): moves.append((r,c,r+d,c+dc))
            if p in "Nn":
                for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<8 and 0<=nc<8:
                        t=board[nr][nc]
                        if t=="." or t.islower()!=p.islower(): moves.append((r,c,nr,nc))
            if p in "BbQq":
                for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                    nr,nc=r+dr,c+dc
                    while 0<=nr<8 and 0<=nc<8:
                        t=board[nr][nc]
                        if t==".": moves.append((r,c,nr,nc))
                        elif t.islower()!=p.islower(): moves.append((r,c,nr,nc));break
                        else: break
                        nr+=dr;nc+=dc
            if p in "RrQq":
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=r+dr,c+dc
                    while 0<=nr<8 and 0<=nc<8:
                        t=board[nr][nc]
                        if t==".": moves.append((r,c,nr,nc))
                        elif t.islower()!=p.islower(): moves.append((r,c,nr,nc));break
                        else: break
                        nr+=dr;nc+=dc
            if p in "Kk":
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if dr==0 and dc==0: continue
                        nr,nc=r+dr,c+dc
                        if 0<=nr<8 and 0<=nc<8:
                            t=board[nr][nc]
                            if t=="." or t.islower()!=p.islower(): moves.append((r,c,nr,nc))
    return moves
def minimax(board,depth,white,alpha=-9999,beta=9999):
    if depth==0: return evaluate(board),None
    moves=gen_moves(board,white)
    if not moves: return evaluate(board),None
    best_move=None
    if white:
        best=-9999
        for m in moves:
            b2=[row[:] for row in board];b2[m[2]][m[3]]=b2[m[0]][m[1]];b2[m[0]][m[1]]="."
            val,_=minimax(b2,depth-1,False,alpha,beta)
            if val>best: best=val;best_move=m
            alpha=max(alpha,val)
            if beta<=alpha: break
    else:
        best=9999
        for m in moves:
            b2=[row[:] for row in board];b2[m[2]][m[3]]=b2[m[0]][m[1]];b2[m[0]][m[1]]="."
            val,_=minimax(b2,depth-1,True,alpha,beta)
            if val<best: best=val;best_move=m
            beta=min(beta,val)
            if beta<=alpha: break
    return best,best_move
if __name__=="__main__":
    board=parse_fen(INIT_BOARD)
    moves=gen_moves(board,True)
    print(f"Starting position: {len(moves)} moves for white")
    assert len(moves)==20
    val,move=minimax(board,2,True)
    print(f"Best move (depth 2): {move}, eval={val}")
    print("Chess engine OK")
