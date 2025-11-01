from itertools import permutations

def solve_cryptarithm(equation: str):
    # Clean spaces and split equation
    equation = equation.replace(" ", "")
    left_side, right_side = equation.split("=")
    addends = left_side.split("+")

    # Collect all unique letters
    letters = sorted(set("".join(addends + [right_side])))

    if len(letters) > 10:
        print(" Too many unique letters (max 10 allowed).")
        return

    print(f"\nSolving Cryptarithm: {equation}")
    print(f"Letters: {letters}")

    # Determine which letters cannot be zero (leading letters)
    leading_letters = set(word[0] for word in addends + [right_side])

    digits = range(10)
    attempts = 0

    # Try all digit permutations for the letters
    for perm in permutations(digits, len(letters)):
        mapping = dict(zip(letters, perm))

        # Constraint: no leading zero in any word
        if any(mapping[l] == 0 for l in leading_letters):
            continue

        attempts += 1

        # Evaluate left and right sides numerically
        left_values = [int("".join(str(mapping[ch]) for ch in word)) for word in addends]
        right_value = int("".join(str(mapping[ch]) for ch in right_side))

        # Check the equation
        if sum(left_values) == right_value:
            print("\n Solution Found!")
            print(f"Attempts Checked: {attempts}\n")

            # Print each letter mapping
            for k in sorted(mapping.keys()):
                print(f"{k} = {mapping[k]}")

            # Display formatted addition layout
            print("\n-----------------------------")
            width = max(len(str(v)) for v in [*left_values, right_value]) + 2
            for i, val in enumerate(left_values):
                prefix = "+" if i == len(left_values) - 1 else " "
                print(f"{prefix}{val:>{width-1}}")
            print("  " + "-" * (width - 1))
            print(f"  {right_value:>{width-1}}")
            print("-----------------------------")
            print(f"\nEquation: {sum(left_values)} = {right_value}")
            return

    print("\n No solution found.")


# ---------- MAIN ----------
if __name__ == "__main__":
    user_input = input("Enter cryptarithm (e.g., SEND+MORE=MONEY): ")
    solve_cryptarithm(user_input)
