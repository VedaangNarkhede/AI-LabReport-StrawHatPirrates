import time
import heapq
from typing import List, Tuple, Optional

State = Tuple[Tuple[int, ...], ...]  # immutable 7x7 board

class Node:
    def __init__(self, st: State, par: Optional["Node"]=None, act=None, g: int=0, h: int=0):
        self.st = st
        self.par = par
        self.act = act
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def to_state(b: List[List[int]]) -> State:
    return tuple(tuple(row) for row in b)

goal_state = to_state([
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2]
])

initial_state = to_state([
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2],
    [1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2]
])

def h1(st: State) -> int:
    return sum(row.count(1) for row in st)

def h2(st: State) -> int:
    return sum(abs(x-3) + abs(y-3) for x in range(7) for y in range(7) if st[x][y] == 1)

def successors(node: Node, heuristic) -> List[Node]:
    res: List[Node] = []
    d_land = [(-2,0),(2,0),(0,-2),(0,2)]
    d_mid  = [(-1,0),(1,0),(0,-1),(0,1)]
    b = node.st
    for x in range(7):
        for y in range(7):
            if b[x][y] != 1:
                continue
            for (dlx,dly),(dmx,dmy) in zip(d_land, d_mid):
                nx, ny = x + dlx, y + dly
                mx, my = x + dmx, y + dmy
                if 0 <= nx < 7 and 0 <= ny < 7 and 0 <= mx < 7 and 0 <= my < 7:
                    if b[mx][my] == 1 and b[nx][ny] == 0:
                        nb = [list(r) for r in b]
                        nb[x][y] = 0
                        nb[mx][my] = 0
                        nb[nx][ny] = 1
                        st = to_state(nb)
                        g = node.g + 1
                        h = heuristic(st)
                        res.append(Node(st, par=node, act=((x,y),(nx,ny)), g=g, h=h))
    return res

def a_star(start: State, goal: State, heuristic):
    start_node = Node(start, g=0, h=heuristic(start))
    frontier = [(start_node.f, 0, start_node)]
    best_g = {start: 0}
    counter, generated, expanded = 1, 0, 0

    while frontier:
        _, _, cur = heapq.heappop(frontier)
        if cur.st == goal:
            return cur, {"generated": generated, "expanded": expanded}
        if cur.g > best_g.get(cur.st, float("inf")):
            continue
        expanded += 1
        for ch in successors(cur, heuristic):
            generated += 1
            prev = best_g.get(ch.st)
            if prev is None or ch.g < prev:
                best_g[ch.st] = ch.g
                heapq.heappush(frontier, (ch.f, counter, ch))
                counter += 1
    return None, {"generated": generated, "expanded": expanded}

def reconstruct(node: Node):
    moves = []
    while node.par:
        moves.append(node.act)
        node = node.par
    return moves[::-1]

if __name__ == "__main__":
    print("A* with heuristic h1")
    t0 = time.time()
    res, stats = a_star(initial_state, goal_state, h1)
    t1 = time.time()
    if res:
        print("Found in", round(t1 - t0, 4), "seconds")
        print("generated:", stats["generated"], "expanded:", stats["expanded"])
        print("cost f:", res.f)
        for m in reconstruct(res): print(m)
    else:
        print("No solution")

    print("\nA* with heuristic h2")
    t0 = time.time()
    res, stats = a_star(initial_state, goal_state, h2)
    t1 = time.time()
    if res:
        print("Found in", round(t1 - t0, 4), "seconds")
        print("generated:", stats["generated"], "expanded:", stats["expanded"])
        print("cost f:", res.f)
        for m in reconstruct(res): print(m)
    else:
        print("No solution")
