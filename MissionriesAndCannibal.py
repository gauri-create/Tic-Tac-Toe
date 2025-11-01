from collections import deque

# Define initial and goal states
initial_state = (3, 3, 1)  # (missionaries_left, cannibals_left, boat_side=1 means left)
goal_state = (0, 0, 0)     # (all moved to right side)

# Define possible moves (missionaries, cannibals)
moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def is_valid(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left

    # No side can have negative or >3 people
    if m_left < 0 or c_left < 0 or m_right < 0 or c_right < 0:
        return False
    if m_left > 3 or c_left > 3 or m_right > 3 or c_right > 3:
        return False

    # Missionaries eaten (if cannibals > missionaries)
    if (m_left > 0 and m_left < c_left) or (m_right > 0 and m_right < c_right):
        return False

    return True


def get_successors(state):
    m, c, boat = state
    successors = []

    for dm, dc in moves:
        if boat == 1:  # Boat on left → move to right
            new_state = (m - dm, c - dc, 0)
        else:          # Boat on right → move to left
            new_state = (m + dm, c + dc, 1)

        if is_valid(new_state):
            successors.append(new_state)
    return successors


def bfs(start, goal):
    queue = deque()
    queue.append((start, [start]))  # (current_state, path)
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state == goal:
            return path

        if current_state in visited:
            continue

        visited.add(current_state)

        for next_state in get_successors(current_state):
            if next_state not in visited:
                queue.append((next_state, path + [next_state]))

    return None


# Run BFS
solution = bfs(initial_state, goal_state)

# Print the solution path
if solution:
    print("Solution found!\n")
    step_num = 1
    for step in solution:
        m, c, boat = step
        side = "Left" if boat == 1 else "Right"
        print(f"Step {step_num}: Missionaries Left = {m}, Cannibals Left = {c}, Boat = {side}")
        step_num += 1
    print(f"\n Total Steps: {len(solution) - 1}")
else:
    print("No solution found.")
