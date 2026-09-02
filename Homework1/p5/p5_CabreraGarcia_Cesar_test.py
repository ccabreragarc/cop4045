# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Unit tests for the interactive Caesar cipher tool

import unittest

import p5_CabreraGarcia_Cesar


class TestCaesarCipher(unittest.TestCase):
    def test_caesar_cipher_preserves_case_and_spaces(self):
        cipher_text = p5_CabreraGarcia_Cesar.caesar_cipher("Cash Ubuntu", 3)
        self.assertEqual(cipher_text, "Fdvk Xexqwx")

    def test_caesar_cipher_wraps_alphabet(self):
        cipher_text = p5_CabreraGarcia_Cesar.caesar_cipher("Zorin OS", 2)
        self.assertEqual(cipher_text, "Bqtkp QU")

    def test_caesar_decipher_returns_clear_text(self):
        clear_text = p5_CabreraGarcia_Cesar.caesar_decipher("Njou", 1)
        self.assertEqual(clear_text, "Mint")

    def test_letter_frequency_ignores_case_and_non_letters(self):
        frequency_report = p5_CabreraGarcia_Cesar.letter_frequency("Cash! cash?")
        self.assertIn("a: 2", frequency_report)
        self.assertIn("c: 2", frequency_report)
        self.assertIn("h: 2", frequency_report)
        self.assertIn("s: 2", frequency_report)
        self.assertIn("b: 0", frequency_report)


if __name__ == "__main__":
    unittest.main()
