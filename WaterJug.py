from collections import deque

def min_steps(m, n, d):
    # If impossible to measure d liters
    if d > max(m, n):
        return -1, []

    # Queue for BFS: (jug1, jug2, steps, path)
    q = deque([(0, 0, 0, [])])

    # For tracking visited states
    visited = [[False] * (n + 1) for _ in range(m + 1)]
    visited[0][0] = True

    while q:
        jug1, jug2, steps, path = q.popleft()

        #  Goal condition: one jug has d liters and the other is empty
        if (jug1 == d and jug2 == 0) or (jug2 == d and jug1 == 0):
            return steps, path + [f"Goal reached: Jug1 = {jug1}L, Jug2 = {jug2}L"]

        # 1. Fill Jug1
        if not visited[m][jug2]:
            visited[m][jug2] = True
            q.append((m, jug2, steps + 1, path + [f"Fill Jug1 -> ({m}, {jug2})"]))

        # 2. Fill Jug2
        if not visited[jug1][n]:
            visited[jug1][n] = True
            q.append((jug1, n, steps + 1, path + [f"Fill Jug2 -> ({jug1}, {n})"]))

        # 3. Empty Jug1
        if not visited[0][jug2]:
            visited[0][jug2] = True
            q.append((0, jug2, steps + 1, path + [f"Empty Jug1 -> (0, {jug2})"]))

        # 4. Empty Jug2
        if not visited[jug1][0]:
            visited[jug1][0] = True
            q.append((jug1, 0, steps + 1, path + [f"Empty Jug2 -> ({jug1}, 0)"]))

        # 5. Pour Jug1 → Jug2
        pour = min(jug1, n - jug2)
        new_jug1 = jug1 - pour
        new_jug2 = jug2 + pour
        if not visited[new_jug1][new_jug2]:
            visited[new_jug1][new_jug2] = True
            q.append((new_jug1, new_jug2, steps + 1,
                      path + [f"Pour Jug1 → Jug2 ({jug1}->{new_jug1}, {jug2}->{new_jug2})"]))

        # 6. Pour Jug2 → Jug1
        pour = min(jug2, m - jug1)
        new_jug1 = jug1 + pour
        new_jug2 = jug2 - pour
        if not visited[new_jug1][new_jug2]:
            visited[new_jug1][new_jug2] = True
            q.append((new_jug1, new_jug2, steps + 1,
                      path + [f"Pour Jug2 → Jug1 ({jug1}->{new_jug1}, {jug2}->{new_jug2})"]))

    return -1, []


if __name__ == "__main__":
    m, n, d = 5, 3, 2
    steps, actions = min_steps(m, n, d)

    if steps == -1:
        print(" It is not possible to measure the desired amount.")
    else:
        print(" Step-by-step process:\n")
        for i, action in enumerate(actions, 1):
            print(f"Step {i}: {action}")
        print("\n Total number of steps followed:", len(actions) - 1)
