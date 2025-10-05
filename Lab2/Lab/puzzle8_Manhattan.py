import heapq

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # cost so far
        self.h = h  # heuristic cost
        self.f = g + h  # total cost
    
    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(state, goal):
    distance = 0
    for value in range(1, 9):
        x1, y1 = divmod(state.index(value), 3)
        x2, y2 = divmod(goal.index(value), 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_successors(node, goal_state):
    successors = []
    zero_index = node.state.index(0)
    moves = [-1, 1, -3, 3]  # left, right, up, down
    
    for move in moves:
        new_index = zero_index + move
        if 0 <= new_index < 9:
            new_state = list(node.state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            g_cost = node.g + 1
            h_cost = manhattan_distance(new_state, goal_state)
            successors.append(Node(new_state, node, g_cost, h_cost))
    
    return successors

def astar(start_state, goal_state):
    start_node = Node(start_state, None, 0, manhattan_distance(start_state, goal_state))
    open_list = []
    heapq.heappush(open_list, start_node)
    visited = set()
    nodes_explored = 0
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if tuple(current_node.state) in visited:
            continue
        
        visited.add(tuple(current_node.state))
        nodes_explored += 1
        
        if current_node.state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            print("Total nodes explored:", nodes_explored)
            return path[::-1]
        
        for successor in get_successors(current_node, goal_state):
            if tuple(successor.state) not in visited:
                heapq.heappush(open_list, successor)
    
    print("Total nodes explored:", nodes_explored)
    return None

start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]

solution = astar(start_state, goal_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
