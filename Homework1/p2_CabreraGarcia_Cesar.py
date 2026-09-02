# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Find all Pythagorean triples up to a user-entered bound

# -----------------------------
# Initial variable declarations
# -----------------------------
n_value = 0
a_value = 0
b_value = 0
c_value = 0
triples = []
triple_index = 0


def find_Pythagorean(n):
    found_triples = []

    # Try every ordered value so both (3, 4, 5) and (4, 3, 5) are included.
    for a_value in range(1, n + 1):
        for b_value in range(1, n + 1):
            for c_value in range(1, n + 1):
                if a_value**2 + b_value**2 == c_value**2:
                    found_triples.append((a_value, b_value, c_value))

    return found_triples


n_value = int(input("Enter n: "))
triples = find_Pythagorean(n_value)

triple_index = 0

while triple_index < len(triples):
    print(triples[triple_index])
    triple_index = triple_index + 1

if len(triples) == 0:
    print("No triples found.")
