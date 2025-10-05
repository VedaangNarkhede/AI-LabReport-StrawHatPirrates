import heapq
import re

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # cost so far
        self.h = h  # heuristic
        self.f = g + h  # total cost
    
    def __lt__(self, other):
        return self.f < other.f

def get_successors(node, doc1, doc2):
    successors = []
    idx1, idx2 = node.state
    
    if idx1 < len(doc1) and idx2 < len(doc2):
        successors.append(Node((idx1 + 1, idx2 + 1), node))
    if idx1 < len(doc1):
        successors.append(Node((idx1 + 1, idx2), node))
    if idx2 < len(doc2):
        successors.append(Node((idx1, idx2 + 1), node))
    
    return successors

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def heuristic(state, doc1, doc2):
    i1, i2 = state
    return (len(doc1) - i1) + (len(doc2) - i2)

def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    return dp[m][n]

def astar(doc1, doc2):
    start_state = (0, 0)
    goal_state = (len(doc1), len(doc2))
    start_node = Node(start_state)
    
    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    explored = set()
    
    while open_list:
        _, current_node = heapq.heappop(open_list)
        
        if current_node.state in explored:
            continue
        
        explored.add(current_node.state)
        
        if current_node.state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]
        
        for successor in get_successors(current_node, doc1, doc2):
            idx1, idx2 = successor.state
            
            if idx1 < len(doc1) and idx2 < len(doc2):
                successor.g = current_node.g + levenshtein(doc1[idx1], doc2[idx2])
            else:
                successor.g = current_node.g + 1
            
            successor.h = heuristic(successor.state, doc1, doc2)
            successor.f = successor.g + successor.h
            heapq.heappush(open_list, (successor.f, successor))
    
    return None

def check_plagiarism(doc1, doc2):
    doc1_clean = [clean_text(sent) for sent in doc1]
    doc2_clean = [clean_text(sent) for sent in doc2]
    
    alignment = astar(doc1_clean, doc2_clean)
    similar_pairs = []
    
    for i, j in alignment:
        if i < len(doc1_clean) and j < len(doc2_clean):
            s1, s2 = doc1_clean[i], doc2_clean[j]
            max_len = max(len(s1), len(s2))
            if max_len > 0:
                similarity = 1 - (levenshtein(s1, s2) / max_len)
                if similarity >= 0.5:
                    similar_pairs.append((doc1[i], doc2[j], similarity))
    
    return similar_pairs

# Example usage
doc1 = [
    "This is a sample document.",
    "Another one comes here.",
]

doc2 = [
    "This is a sample doc.",
    "This one might be copied.",
]

plagiarism = check_plagiarism(doc1, doc2)

if plagiarism:
    print("Potential plagiarism detected:")
    for pair in plagiarism:
        print(f"Doc1: {pair[0]}\nDoc2: {pair[1]}\nSimilarity: {pair[2]*100:.2f}%\n")
else:
    print("No plagiarism detected.")
