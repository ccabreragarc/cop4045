# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Test weather validation, statistics, ordering, and CLI errors

import contextlib
import csv
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import p5_CabreraGarcia_Cesar as weather


class WeatherStationTests(unittest.TestCase):
    """Exercise file contracts and calculations using isolated temporary files."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.source = Path(self.directory.name) / "Cash.csv"
        self.destination = Path(self.directory.name) / "Mint.csv"

    def read_rows(self, text):
        self.source.write_text(text, encoding="utf-8")
        return weather.read_observations(str(self.source))

    def test_multiple_stations_and_chronological_order(self):
        observations, errors = self.read_rows(
            "Ubuntu,01:00:00 AM 01/01/2026,10\n"
            "Mint,12:00:00 PM 04/20/2026,-5\n"
            "Ubuntu,11:00:00 PM 12/31/2025,-10\n"
        )
        self.assertEqual(errors, [])
        self.assertEqual(list(observations), ["Ubuntu", "Mint"])
        self.assertEqual(observations["Ubuntu"][0], ("11:00:00 PM 12/31/2025", -10.0))

    def test_duplicates_use_parsed_dates_and_keep_first_valid(self):
        observations, errors = self.read_rows(
            "Cash,09:00:00 AM 04/20/2026,invalid\n"
            "Cash,09:00:00 AM 04/20/2026,1\n"
            "Cash,9:00:00 AM 4/20/2026,2\n"
            "Mint,09:00:00 AM 04/20/2026,3\n"
        )
        self.assertEqual([number for number, _ in errors], [1, 3])
        self.assertEqual(observations["Cash"], [("09:00:00 AM 04/20/2026", 1.0)])
        self.assertIn("Mint", observations)

    def test_temperature_boundaries_and_nonfinite_values(self):
        rows = "".join(
            f"Cash,09:00:00 AM 04/{day:02d}/2026,{value}\n"
            for day, value in enumerate(["-100", "150", "-100.1", "150.1", "nan", "inf", "-inf"], 1)
        )
        observations, errors = self.read_rows(rows)
        self.assertEqual([value for _, value in observations["Cash"]], [-100.0, 150.0])
        self.assertEqual([number for number, _ in errors], [3, 4, 5, 6, 7])

    def test_malformed_rows_invalid_dates_and_recovery(self):
        observations, errors = self.read_rows(
            "\n"
            "Cash,09:00:00 AM 04/20/2026\n"
            "Cash,09:00:00 AM 04/20/2026,1,2\n"
            "Cash,09:00:00 AM 02/30/2026,1\n"
            ",09:00:00 AM 04/20/2026,1\n"
            '"Cash,09:00:00 AM 04/20/2026,1\n'
            "Mint,09:00:00 AM 04/20/2026,7\n"
        )
        self.assertEqual([number for number, _ in errors], [1, 2, 3, 4, 5, 6])
        self.assertEqual(observations, {"Mint": [("09:00:00 AM 04/20/2026", 7.0)]})

    def test_statistics_negative_temperatures_and_outliers(self):
        observations, _ = self.read_rows(
            "Cash,09:00:00 AM 04/20/2026,-10\n"
            "Cash,09:00:00 AM 04/21/2026,2\n"
            "Mint,09:00:00 AM 04/20/2026,3\n"
        )
        self.assertEqual(weather.station_statistics(observations), {
            "Cash": (-10.0, 2.0, -4.0), "Mint": (3.0, 3.0, 3.0),
        })
        # Latest must be determined by date even if a caller supplies unsorted data.
        observations["Cash"].reverse()
        self.assertEqual(weather.station_outliers(observations), {
            "Cash": ("09:00:00 AM 04/21/2026", 2.0, -4.0),
        })

    def test_sorted_output_and_exact_decimal_precision(self):
        weather.write_statistics(str(self.destination), {
            "Zorin OS": (0.0, 1.0, 1 / 3), "Cash": (-12.25, 10, -1.125),
        })
        with self.destination.open(newline="", encoding="utf-8") as output:
            self.assertEqual(list(csv.reader(output)), [
                ["station", "min", "max", "mean"],
                ["Cash", "-12.2", "10.0", "-1.1"],
                ["Zorin OS", "0.0", "1.0", "0.3"],
            ])

    def test_missing_input_and_unwritable_output(self):
        with self.assertRaises(FileNotFoundError):
            weather.read_observations(str(self.source))
        with self.assertRaises(OSError):
            weather.write_statistics(self.directory.name, {})

    def test_empty_file_and_empty_station(self):
        self.assertEqual(self.read_rows(""), ({}, []))
        self.assertEqual(weather.station_statistics({"Cash": []}), {})
        self.assertEqual(weather.station_outliers({"Cash": []}), {})
        weather.write_statistics(str(self.destination), {})
        self.assertEqual(self.destination.read_text(), "station,min,max,mean\n")

    def test_cli_file_error_is_graceful(self):
        with patch("sys.argv", ["weather", str(self.source), str(self.destination)]):
            with contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(weather.main(), 1)
        self.assertIn("[ERROR]", output.getvalue())

    def test_cli_success_and_source_overwrite_protection(self):
        text = "Cash,09:00:00 AM 04/20/2026,2\n"
        self.source.write_text(text, encoding="utf-8")
        with patch("sys.argv", ["weather", str(self.source), str(self.destination)]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(weather.main(), 0)
        self.assertTrue(self.destination.exists())
        with patch("sys.argv", ["weather", str(self.source), str(self.source)]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(weather.main(), 2)
        self.assertEqual(self.source.read_text(), text)


if __name__ == "__main__":
    unittest.main()
