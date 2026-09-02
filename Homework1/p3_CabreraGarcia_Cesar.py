# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Locate duplicated substrings in user-entered text

# -----------------------------
# Initial variable declarations
# -----------------------------
s = ""
n_value = 0
duplicated_substring = ""
maximum_duplicated_substring = ""


def find_dup_str(s, n):
    text_length = 0
    start_one = 0
    start_two = 0
    first_piece = ""
    second_piece = ""

    for current_character in s:
        text_length = text_length + 1

    if n <= 0:
        return ""

    # Start the second substring after the first one ends so they do not overlap.
    while start_one <= text_length - n:
        first_piece = s[start_one:start_one + n]
        start_two = start_one + n

        while start_two <= text_length - n:
            second_piece = s[start_two:start_two + n]

            if first_piece == second_piece:
                return first_piece

            start_two = start_two + 1

        start_one = start_one + 1

    return ""


def find_max_dup(s):
    text_length = 0
    current_length = 0
    current_result = ""

    for current_character in s:
        text_length = text_length + 1

    current_length = text_length - 1

    # Search from longest to shortest so the first match is the answer.
    while current_length > 0:
        current_result = find_dup_str(s, current_length)

        if current_result != "":
            return current_result

        current_length = current_length - 1

    return ""


s = input("Enter string: ")
n_value = int(input("Enter substring length: "))

duplicated_substring = find_dup_str(s, n_value)
print("Duplicated substring:", duplicated_substring)

maximum_duplicated_substring = find_max_dup(s)
print("Longest duplicated substring:", maximum_duplicated_substring)
