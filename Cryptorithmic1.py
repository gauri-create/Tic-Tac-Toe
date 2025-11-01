# CSP for cryptarithmetic problem
# SEND + MORE = MONEY

import os
import random

# Clear screen (cross-platform)
os.system("cls" if os.name == "nt" else "clear")

print("Cryptarithmetic Puzzle: SEND + MORE = MONEY")

count = 0

while True:
    count += 1

    digits = list(range(10))
    random.shuffle(digits)

    # Assign random digits to each letter
    S = digits.pop()
    E = digits.pop()
    N = digits.pop()
    D = digits.pop()
    M = digits.pop()
    O = digits.pop()
    R = digits.pop()
    Y = digits.pop()

    # Constraints: S and M cannot be zero
    if S == 0 or M == 0:
        continue

    # Construct numbers
    SEND = S * 1000 + E * 100 + N * 10 + D
    MORE = M * 1000 + O * 100 + R * 10 + E
    MONEY = M * 10000 + O * 1000 + N * 100 + E * 10 + Y

    # Check the main equation
    if SEND + MORE == MONEY:
        print("\n✅ Solution Found!")
        print(f"Attempts: {count}\n")
        print(f"   {S}{E}{N}{D}")
        print(f"+  {M}{O}{R}{E}")
        print("  ________________")
        print(f"  {M}{O}{N}{E}{Y}")
        break
