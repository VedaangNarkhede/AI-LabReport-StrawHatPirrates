from collections import deque

def get_successors(state):
    moves = []
    for i, val in enumerate(state):
        if val == 1:  # frog facing right
            if i + 1 < len(state) and state[i + 1] == 0:
                new_state = list(state)
                new_state[i], new_state[i + 1] = 0, 1
                moves.append(tuple(new_state))
            if i + 2 < len(state) and state[i + 2] == 0:
                new_state = list(state)
                new_state[i], new_state[i + 2] = 0, 1
                moves.append(tuple(new_state))
        elif val == -1:  # frog facing left
            if i - 1 >= 0 and state[i - 1] == 0:
                new_state = list(state)
                new_state[i], new_state[i - 1] = 0, -1
                moves.append(tuple(new_state))
            if i - 2 >= 0 and state[i - 2] == 0:
                new_state = list(state)
                new_state[i], new_state[i - 2] = 0, -1
                moves.append(tuple(new_state))
    return moves

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()
    
    while stack:
        state, path = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal:
            print("Total nodes explored:", len(visited))
            return path
        for next_state in get_successors(state):
            stack.append((next_state, path))
    return None

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()
    
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal:
            print("Total nodes explored:", len(visited))
            return path
        for next_state in get_successors(state):
            queue.append((next_state, path))
    return None

start_state = (1, 1, 1, 0, -1, -1, -1)
goal_state = (-1, -1, -1, 0, 1, 1, 1)

print("Depth-First Search (DFS) Solution:")
dfs_solution = dfs(start_state, goal_state)
if dfs_solution:
    print("Solution found!")
    print("Steps count:", len(dfs_solution) - 1)
    for step in dfs_solution:
        print(step)
else:
    print("No solution exists.")

print("\nBreadth-First Search (BFS) Solution:")
bfs_solution = bfs(start_state, goal_state)
if bfs_solution:
    print("Solution found!")
    print("Steps count:", len(bfs_solution) - 1)
    for step in bfs_solution:
        print(step)
else:
    print("No solution exists.")
