# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Solve six list and dictionary comprehension exercises

student_name = "Cesar Cabrera Garcia"
lower_bound = 1
upper_bound = 10
words = ["Cash", "Ubuntu", "Mint", "Zorin OS"]
names = ["Cash Ubuntu Mint", "Ubuntu Mint Cash"]
first_words = ["Cash", "Ubuntu", "Mint"]
second_words = ["CASH", "MINT", "Zorin OS"]
distinct_words = ["Cash", "Ubuntu", "Mint"]
text = "Cash Ubuntu Mint Zorin OS"

# Keep every ordering because the question asks for all distinct quadruples.
equal_squares = [
    (a, b, c, d)
    for a in range(lower_bound, upper_bound + 1)
    for b in range(lower_bound, upper_bound + 1)
    for c in range(lower_bound, upper_bound + 1)
    for d in range(lower_bound, upper_bound + 1)
    if a != b and a != c and a != d and b != c and b != d and c != d
    and a**2 + b**2 == c**2 + d**2
]
short_words = [(word.lower(), len(word)) for word in words if len(word) < 5]
abbreviated_names = [
    name.split()[0] + " " + name.split()[1][0] + ". " + name.split()[2]
    for name in names
]
# Sorted letters preserve repeated letters, which an anagram must also match.
anagram_pairs = [
    (word_one, word_two)
    for word_one in first_words
    for word_two in second_words
    if sorted(word_one.lower()) == sorted(word_two.lower())
]
word_lengths = {word: len(word) for word in distinct_words}
vowel_positions = {
    index: text[index] for index in range(len(text))
    if text[index].lower() in "aeiou"
}


def main() -> None:
    """Display the results of all six comprehensions."""
    print(student_name)
    print("[STATUS] Comprehension results")
    print("a)", equal_squares)
    print("b)", short_words)
    print("c)", abbreviated_names)
    print("d)", anagram_pairs)
    print("e)", word_lengths)
    print("f)", vowel_positions)


if __name__ == "__main__":
    main()
