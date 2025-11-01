import heapq 
 
# Define the goal state for the 8-puzzle 
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] 
 
# Directions for moving the empty tile (up, down, left, right) 
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
 
# Helper function to find the position of '0' (the empty tile) in the puzzle 
def find_blank(state): 
    for r in range(3): 
        for c in range(3): 
            if state[r][c] == 0: 
                return r, c 
    return None 
 
# Manhattan Distance Heuristic 
def manhattan_distance(state): 
    distance = 0 
    for r in range(3): 
        for c in range(3): 
            value = state[r][c] 
            if value != 0: 
                goal_r, goal_c = divmod(value - 1, 3) 
                distance += abs(goal_r - r) + abs(goal_c - c) 
    return distance 
 
# Check if the state is the goal state 
def is_goal(state): 
    return state == GOAL_STATE 
 
# Generate possible moves for the puzzle 
def get_neighbors(state): 
    neighbors = [] 
    blank_r, blank_c = find_blank(state) 
     
    for move in MOVES: 
        new_r, new_c = blank_r + move[0], blank_c + move[1] 
        if 0 <= new_r < 3 and 0 <= new_c < 3: 
            new_state = [row[:] for row in state]  # Deep copy of the state 
            new_state[blank_r][blank_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[blank_r][blank_c] 
            neighbors.append(new_state) 
     
    return neighbors 
 
# Helper: Convert state to tuple (for hashing in visited dicts) 
def state_to_tuple(state): 
    return tuple(tuple(row) for row in state) 
 
# Pretty print a state 
def print_state(state): 
    for row in state: 
        print(row) 
    print("-" * 10) 
 
# A* Search Algorithm 
def a_star(start_state): 
    # Priority Queue to store (f, g, state) tuples 
    open_list = [] 
    heapq.heappush(open_list, (manhattan_distance(start_state), 0, start_state)) 
     
    # Dictionary to keep track of visited states and their g values 
    visited = {} 
    visited[state_to_tuple(start_state)] = 0 
     
    # Dictionary to store parent relationships (for path reconstruction) 
    parent = {} 
    parent[state_to_tuple(start_state)] = None 
     
    while open_list: 
        f, g, current_state = heapq.heappop(open_list) 
         
        # If the current state is the goal, reconstruct path 
        if is_goal(current_state): 
            path = [] 
            state_tuple = state_to_tuple(current_state) 
            while state_tuple is not None: 
                path.append([list(row) for row in state_tuple]) 
                state_tuple = parent[state_tuple] 
            path.reverse()  # From start to goal 
            return path 
         
        # Explore neighbors 
        for neighbor in get_neighbors(current_state): 
            new_g = g + 1 
            neighbor_tuple = state_to_tuple(neighbor) 
             
            if neighbor_tuple not in visited or new_g < visited[neighbor_tuple]: 
                visited[neighbor_tuple] = new_g 
                parent[neighbor_tuple] = state_to_tuple(current_state) 
                f = new_g + manhattan_distance(neighbor) 
                heapq.heappush(open_list, (f, new_g, neighbor)) 
     
    return None  # No solution found 
 
# Example usage 
if __name__ == "__main__": 
    start_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]] 
     
    solution_path = a_star(start_state) 
    if solution_path: 
        print(f"Solution found in {len(solution_path)-1} moves.\n") 
        for step, state in enumerate(solution_path): 
            print(f"Step {step}:") 
            print_state(state) 
    else: 
        print("No solution exists.") 