import time
import heapq

class Node:
    def __init__(self, st, par=None, g=0):
        self.st = st
        self.par = par
        self.act = None
        self.g = g
    def __lt__(self, o):
        return self.g < o.g

goal = [
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2]
]

start = [
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2],
    [1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [2,2,1,1,1,2,2],
    [2,2,1,1,1,2,2]
]

cnt = 0

def succ(n):
    global cnt
    res = []
    d1 = [(-2,0),(2,0),(0,-2),(0,2)]
    d2 = [(-1,0),(1,0),(0,-1),(0,1)]
    for i in range(7):
        for j in range(7):
            if n.st[i][j] == 1:
                for d in range(4):
                    nx, ny = i+d1[d][0], j+d1[d][1]
                    mx, my = i+d2[d][0], j+d2[d][1]
                    if 0<=nx<7 and 0<=ny<7 and n.st[mx][my]==1 and n.st[nx][ny]==0:
                        ns = [row[:] for row in n.st]
                        ns[i][j] = 0
                        ns[mx][my] = 0
                        ns[nx][ny] = 1
                        c = Node(ns, n, g=n.g+1)
                        c.act = [(i,j),(nx,ny)]
                        res.append(c)
                        cnt += 1
    return res

def search():
    fr = []
    seen = set()
    s = Node(start)
    heapq.heappush(fr, s)
    while fr:
        cur = heapq.heappop(fr)
        print("g:", cur.g)
        for r in cur.st: print(r)
        print()
        if cur.st == goal:
            print("done")
            return cur
        seen.add(str(cur.st))
        for ch in succ(cur):
            if str(ch.st) not in seen:
                heapq.heappush(fr, ch)
    return None

def path(n):
    res = []
    while n.par:
        res.append(n.act)
        n = n.par
    return res[::-1]

print("search start")
st = time.time()
res = search()
et = time.time()
if res:
    print("nodes:", cnt)
    print("time:", et-st)
    print("final:")
    for r in res.st: print(r)
    print("\nmoves:")
    for m in path(res):
        print(m)
else:
    print("no sol")
