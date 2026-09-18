# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Independently verify Homework 2 problems 1 through 4

import contextlib
import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import p1_CabreraGarcia_Cesar as parser
import p2_CabreraGarcia_Cesar as comprehensions
import p3_CabreraGarcia_Cesar as network
import p4_CabreraGarcia_Cesar as movies


class HomeworkTests(unittest.TestCase):
    def test_line_numbers_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "Cash.py"
            destination = Path(directory) / "Cash.txt"
            source.write_text("Cash\n\nUbuntu", encoding="utf-8")
            parser.line_number(str(source), str(destination))
            self.assertEqual(destination.read_text(), "1. Cash\n2. \n3. Ubuntu")
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    parser.line_number(str(source), str(source))
            self.assertEqual(source.read_text(), "Cash\n\nUbuntu")

    def test_parser_preserves_strings_and_multiline_arguments(self):
        source_text = (
            '# Cash\n'
            'def Ubuntu(\n'
            '    text="Cash#",\n'
            '    count=(1 + 2)\n'
            '): # Ubuntu\n'
            '    """Cash\n\nUbuntu"""\n'
            '    # Mint\n'
            '\n'
            '    return text # Cash\n'
            '\n'
            'def Cash():\n'
            '    return "Mint"\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "Cash.py"
            source.write_text(source_text, encoding="utf-8")
            records = parser.parse_functions(str(source))
        self.assertEqual([record[1] for record in records], ["Cash", "Ubuntu"])
        self.assertEqual(records[1][0], 2)
        self.assertIn('text="Cash#"', records[1][2])
        self.assertIn("count=(1 + 2)", records[1][2])
        self.assertNotIn("# Ubuntu", records[1][3])
        self.assertNotIn("# Mint", records[1][3])
        self.assertIn('"""Cash\n\nUbuntu"""', records[1][3])
        self.assertTrue(records[1][3].endswith("return text\n"))

    def test_parser_nested_functions_and_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "Cash.py"
            source.write_text("def Ubuntu():\n    def Cash():\n        return 1\n    return Cash()\n")
            records = parser.parse_functions(str(source))
            self.assertEqual([record[1] for record in records], ["Cash", "Ubuntu"])
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(FileNotFoundError):
                    parser.parse_functions(str(Path(directory) / "Mint.py"))

    def test_comprehension_results(self):
        self.assertEqual(len(comprehensions.equal_squares), 16)
        self.assertEqual(len(set(comprehensions.equal_squares)), 16)
        for a, b, c, d in comprehensions.equal_squares:
            self.assertEqual(len({a, b, c, d}), 4)
            self.assertTrue(all(1 <= value <= 10 for value in (a, b, c, d)))
            self.assertEqual(a * a + b * b, c * c + d * d)
        self.assertEqual(comprehensions.short_words, [("cash", 4), ("mint", 4)])
        self.assertEqual(comprehensions.abbreviated_names, ["Cash U. Mint", "Ubuntu M. Cash"])
        self.assertEqual(comprehensions.anagram_pairs, [("Cash", "CASH"), ("Mint", "MINT")])
        self.assertEqual(comprehensions.word_lengths, {"Cash": 4, "Ubuntu": 6, "Mint": 4})
        self.assertEqual(comprehensions.vowel_positions, {
            1: "a", 5: "U", 7: "u", 10: "u", 13: "i", 18: "o", 20: "i", 23: "O",
        })

    def test_network_extra_credit_and_duplicate_edges(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(network.test())
        sn = {"Cash": ("Cash", []), "Mint": ("Mint", [])}
        network.add_friend(sn, "Cash", "Mint")
        network.add_friend(sn, "Cash", "Mint")
        self.assertEqual(sn["Cash"][1], ["Mint"])
        self.assertEqual(network.get_friends(sn, "Cash", 100), ["Mint"])

    def test_network_csv_quoting_and_broken_links(self):
        sn = {"Cash": ('Cash, "Ubuntu"', ["Mint"]), "Mint": ("Mint", ["Cash"])}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Cash.csv"
            network.save_network(str(path), sn)
            self.assertEqual(network.load_network(str(path)), sn)
            path.write_text("Cash,Cash,Mint\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    network.load_network(str(path))

    def test_movie_join_uses_year_and_does_not_double_count_actor(self):
        with tempfile.TemporaryDirectory() as directory:
            rated = Path(directory) / "Ubuntu.csv"
            grossing = Path(directory) / "Mint.csv"
            casts = Path(directory) / "Cash.csv"
            rated.write_text("Rank,Title,Year,Rating\n1,Cash,2025,9\n2,Ubuntu,2026,8\n")
            grossing.write_text("Rank,Title,Year,Gross\n1,Cash,2025,100\n2,Ubuntu,2026,200\n")
            casts.write_text(
                "Cash,2025,Mint,Ubuntu,Ubuntu,Cash\n"
                "Cash,2026,Zorin OS,Mint\n"
                "Ubuntu,2026,Mint,Ubuntu\n"
            )
            with patch.multiple(movies, rated_filename=str(rated), grossing_filename=str(grossing), casts_filename=str(casts)):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    movies.display_top_collaborations(1)
                self.assertEqual(output.getvalue().splitlines()[1:], ["1 ('Mint', 'Ubuntu', 2)"])
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    movies.display_top_actors()
                self.assertEqual(output.getvalue().splitlines()[1:], ["1. Ubuntu: $300", "2. Cash: $100"])


if __name__ == "__main__":
    unittest.main()
