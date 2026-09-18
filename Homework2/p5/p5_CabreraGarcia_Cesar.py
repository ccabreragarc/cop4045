# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Validate weather observations and report station statistics

"""Analyze headerless station,date,temperature CSV files using local timestamps."""

import csv
from datetime import datetime
from pathlib import Path
from statistics import fmean
import sys

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MIN_TEMPERATURE = -100.0
MAX_TEMPERATURE = 150.0
AUTHOR = "Cesar Cabrera Garcia"

Observations = dict[str, list[tuple[str, float]]]
Statistics = dict[str, tuple[float, float, float]]


def read_observations(filename: str) -> tuple[Observations, list[tuple[int, str]]]:
    """Read valid observations and collect errors using one-based line numbers.

    Dates retain their input spelling but are validated and sorted as datetimes.
    The first valid observation wins when a station/timestamp is repeated.
    File-access and encoding failures propagate to the caller.
    """
    observations: Observations = {}
    errors: list[tuple[int, str]] = []
    seen: set[tuple[str, datetime]] = set()

    with open(filename, encoding="utf-8-sig", newline="") as source:
        for line_number, line in enumerate(source, start=1):
            try:
                # Records occupy one physical line, allowing recovery after bad CSV.
                row = next(csv.reader([line], strict=True))
                if len(row) != 3:
                    raise ValueError("Expected station,date,temperature.")
                station, date_text, temperature_text = (value.strip() for value in row)
                if not station:
                    raise ValueError("Station name cannot be empty.")
                try:
                    timestamp = datetime.strptime(date_text, DATE_FORMAT)
                except ValueError as error:
                    raise ValueError("Invalid date; expected HH:MM:SS AM/PM MM/DD/YYYY.") from error
                try:
                    temperature = float(temperature_text)
                except ValueError as error:
                    raise ValueError("Temperature must be a number.") from error
                # This also rejects NaN and infinities without special cases.
                if not MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE:
                    raise ValueError("Temperature must be between -100.0 and 150.0.")
                key = (station, timestamp)
                if key in seen:
                    raise ValueError("Duplicate station/date observation.")
                seen.add(key)
                observations.setdefault(station, []).append((date_text, temperature))
            except (ValueError, csv.Error) as error:
                errors.append((line_number, str(error)))

    for records in observations.values():
        records.sort(key=lambda record: datetime.strptime(record[0], DATE_FORMAT))
    return observations, errors


def station_statistics(observations: Observations) -> Statistics:
    """Map each nonempty station to (minimum, maximum, mean) temperatures."""
    statistics: Statistics = {}
    for station, records in observations.items():
        if records:
            temperatures = [temperature for _, temperature in records]
            statistics[station] = (min(temperatures), max(temperatures), fmean(temperatures))
    return statistics


def station_outliers(observations: Observations) -> dict[str, tuple[str, float, float]]:
    """Return stations whose chronologically latest temperature exceeds their mean."""
    statistics = station_statistics(observations)
    latest = {
        station: max(records, key=lambda record: datetime.strptime(record[0], DATE_FORMAT))
        for station, records in observations.items() if records
    }
    return {
        station: (latest[station][0], latest[station][1], statistics[station][2])
        for station in sorted(latest)
        if latest[station][1] > statistics[station][2]
    }


def write_statistics(filename: str, statistics: Statistics) -> None:
    """Write station,min,max,mean CSV rows alphabetically, with one decimal place.

    The output includes a header. Individual observations are not part of the
    statistics argument; input observations are ordered by read_observations.
    File-access failures propagate to the caller.
    """
    with open(filename, "w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(("station", "min", "max", "mean"))
        for station in sorted(statistics):
            writer.writerow((station, *(f"{value:.1f}" for value in statistics[station])))


def main() -> int:
    """Read sys.argv paths, print results, and return a command-line exit status."""
    if len(sys.argv) != 3:
        print(f"Usage: {Path(sys.argv[0]).name} INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2

    source, destination = map(Path, sys.argv[1:])
    try:
        if source.resolve() == destination.resolve() or (
            destination.exists() and source.samefile(destination)
        ):
            print("[ERROR] Input and output must be different files.", file=sys.stderr)
            return 2
        observations, errors = read_observations(str(source))
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)
        print(AUTHOR)
        for line_number, message in errors:
            print(f"[WARNING] Line {line_number}: {message}")
        print("Station | Minimum | Maximum | Mean")
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            print(f"{station} | {minimum:.1f} | {maximum:.1f} | {mean:.1f}")
        print("Outliers (latest temperature above station mean):")
        for station, (date_text, temperature, mean) in outliers.items():
            print(f"{station} | {date_text} | {temperature:.1f} | mean {mean:.1f}")
        if not outliers:
            print("None")
        write_statistics(str(destination), statistics)
        print(f"[INFO] Wrote {len(statistics)} stations to {destination}.")
        return 0
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"[ERROR] Could not process the weather files: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
