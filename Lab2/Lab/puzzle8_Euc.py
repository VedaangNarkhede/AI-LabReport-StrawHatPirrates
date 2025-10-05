from collections import deque

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    successors = []
    zero_index = node.state.index(0)
    moves = [-1, 1, -3, 3]  # left, right, up, down
    
    for move in moves:
        new_index = zero_index + move
        if 0 <= new_index < 9:
            new_state = list(node.state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            successors.append(Node(new_state, node))
    
    return successors

def bfs(start_state, goal_state):
    start_node = Node(start_state)
    goal_node = Node(goal_state)
    queue = deque([start_node])
    visited = set()
    nodes_explored = 0
    
    while queue:
        current_node = queue.popleft()
        
        if tuple(current_node.state) in visited:
            continue
        
        visited.add(tuple(current_node.state))
        nodes_explored += 1
        print(current_node.state)
        
        if current_node.state == goal_node.state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            print("Total nodes explored:", nodes_explored)
            return path[::-1]
        
        for successor in get_successors(current_node):
            queue.append(successor)
    
    print("Total nodes explored:", nodes_explored)
    return None

start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]

solution = bfs(start_state, goal_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
