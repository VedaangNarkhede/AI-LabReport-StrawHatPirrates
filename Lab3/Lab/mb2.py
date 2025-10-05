import time
import heapq
from typing import List, Tuple, Optional

State = Tuple[Tuple[int, ...], ...]

class Node:
    __slots__ = ("st","par","g","act")
    def __init__(self, st: State, par: Optional["Node"]=None, g: int=0, act=None):
        self.st = st
        self.par = par
        self.g = g
        self.act = act
    def __lt__(self, other):
        return self.g < other.g

def to_state(b: List[List[int]]) -> State:
    return tuple(tuple(row) for row in b)

goal = to_state([
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
])

start = to_state([
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2],
    [1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2],
])

def succ(n: Node) -> List[Node]:
    res = []
    d_land = [(-2,0),(2,0),(0,-2),(0,2)]
    d_mid  = [(-1,0),(1,0),(0,-1),(0,1)]
    b = n.st
    for x in range(7):
        for y in range(7):
            if b[x][y] != 1:
                continue
            for (dlx,dly),(dmx,dmy) in zip(d_land,d_mid):
                nx, ny = x+dlx, y+dly
                mx, my = x+dmx, y+dmy
                if 0<=nx<7 and 0<=ny<7 and 0<=mx<7 and 0<=my<7:
                    if b[mx][my]==1 and b[nx][ny]==0:
                        nb = [list(r) for r in b]
                        nb[x][y] = 0
                        nb[mx][my] = 0
                        nb[nx][ny] = 1
                        st = to_state(nb)
                        res.append(Node(st, n, g=n.g+1, act=((x,y),(nx,ny))))
    return res

def h_count_mismatch(s: State) -> int:
    mism = 0
    for i in range(7):
        for j in range(7):
            if s[i][j] == 1 and goal[i][j] == 0:
                mism += 1
    return mism

def best_first(start_st: State, goal_st: State):
    t0 = time.time()
    heap = []
    entry_count = 0
    start_node = Node(start_st, g=0)
    heapq.heappush(heap, (h_count_mismatch(start_st), entry_count, start_node))
    entry_count += 1
    best_seen = {start_st: 0}
    generated = 0
    expanded = 0

    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur.st == goal_st:
            return cur, {"generated": generated, "expanded": expanded, "time": time.time()-t0}
        if best_seen.get(cur.st, float("inf")) < cur.g:
            continue
        expanded += 1
        for ch in succ(cur):
            generated += 1
            prev = best_seen.get(ch.st)
            if prev is None or ch.g < prev:
                best_seen[ch.st] = ch.g
                heapq.heappush(heap, (h_count_mismatch(ch.st), entry_count, ch))
                entry_count += 1
    return None, {"generated": generated, "expanded": expanded, "time": time.time()-t0}

def reconstruct(n: Node):
    moves = []
    while n.par:
        moves.append(n.act)
        n = n.par
    moves.reverse()
    return moves

if __name__ == "__main__":
    print("Best-First Search started")
    res, stats = best_first(start, goal)
    if res:
        print("Done")
        print("time:", round(stats["time"], 4))
        print("nodes_generated:", stats["generated"])
        print("nodes_expanded:", stats["expanded"])
        print("final:")
        for r in res.st:
            print(r)
        print("\nmoves:")
        for m in reconstruct(res):
            print(m)
    else:
        print("No solution found.")
