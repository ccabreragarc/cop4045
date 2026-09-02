# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Interactive Caesar cipher tool with letter frequency reporting

import string


ALPHABET_LENGTH = 26
LOWERCASE_ALPHABET = string.ascii_lowercase
UPPERCASE_ALPHABET = string.ascii_uppercase


def caesar_cipher(text, shift):
    encrypted_text = ""
    normalized_shift = shift % ALPHABET_LENGTH

    for current_character in text:
        if current_character in LOWERCASE_ALPHABET:
            original_index = LOWERCASE_ALPHABET.index(current_character)
            shifted_index = (original_index + normalized_shift) % ALPHABET_LENGTH
            encrypted_text = encrypted_text + LOWERCASE_ALPHABET[shifted_index]
        elif current_character in UPPERCASE_ALPHABET:
            original_index = UPPERCASE_ALPHABET.index(current_character)
            shifted_index = (original_index + normalized_shift) % ALPHABET_LENGTH
            encrypted_text = encrypted_text + UPPERCASE_ALPHABET[shifted_index]
        else:
            encrypted_text = encrypted_text + current_character

    return encrypted_text


def caesar_decipher(cyphertext, shift):
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    frequency_report = ""

    for current_letter in LOWERCASE_ALPHABET:
        letter_count = 0

        for current_character in text:
            if current_character.lower() == current_letter:
                letter_count = letter_count + 1

        frequency_report = frequency_report + current_letter + ": " + str(letter_count)

        if current_letter != "z":
            frequency_report = frequency_report + "\n"

    return frequency_report


def main():
    print("Caesar Cipher Tool")

    while True:
        print("")
        print("1. Encrypt, analyze, and decrypt a message")
        print("2. Quit")
        menu_choice = input("Enter menu option: ")

        if menu_choice == "1":
            plain_text = input("Enter message: ")
            shift_value = int(input("Enter shift value: "))

            cipher_text = caesar_cipher(plain_text, shift_value)
            frequency_report = letter_frequency(cipher_text)
            deciphered_text = caesar_decipher(cipher_text, shift_value)

            print("")
            print("Ciphered text:")
            print(cipher_text)
            print("")
            print("Letter frequency breakdown:")
            print(frequency_report)
            print("")
            print("Deciphered text:")
            print(deciphered_text)
        elif menu_choice == "2":
            print("Program finished.")
            break
        else:
            print("Invalid menu option. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
