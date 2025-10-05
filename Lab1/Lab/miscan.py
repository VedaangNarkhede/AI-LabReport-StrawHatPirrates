from collections import deque
import time

start_time = time.time()

def is_valid(state):
    missionaries, cannibals, _ = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and 3 - missionaries < 3 - cannibals:
        return False
    return True

def get_successors(state):
    missionaries, cannibals, boat = state
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    successors = []
    
    if boat == 1:
        for m, c in moves:
            new_state = (missionaries - m, cannibals - c, 0)
            if is_valid(new_state):
                successors.append(new_state)
    else:
        for m, c in moves:
            new_state = (missionaries + m, cannibals + c, 1)
            if is_valid(new_state):
                successors.append(new_state)
    
    return successors

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()
    
    while queue:
        current_state, path = queue.popleft()
        
        if current_state in visited:
            continue
        
        visited.add(current_state)
        path = path + [current_state]
        
        if current_state == goal:
            return path
        
        for successor in get_successors(current_state):
            queue.append((successor, path))
    
    return None

start_state = (3, 3, 1)
goal_state = (0, 0, 0)

solution = bfs(start_state, goal_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution exists.")

end_time = time.time()
print(f"Total runtime: {end_time - start_time:.4f} seconds")
