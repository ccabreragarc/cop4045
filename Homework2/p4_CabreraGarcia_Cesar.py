# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Rank movie collaborations and actor box-office totals

import csv
import os

student_name = "Cesar Cabrera Garcia"
data_directory = os.path.dirname(os.path.abspath(__file__))
rated_filename = os.path.join(data_directory, "imdb-top-rated.csv")
grossing_filename = os.path.join(data_directory, "imdb-top-grossing.csv")
casts_filename = os.path.join(data_directory, "imdb-top-casts.csv")
display_limit = 10


def read_movies(filename: str) -> dict:
    """Index a ranked movie file by (title, year), retaining the value column."""
    movies = {}
    with open(filename, "r", newline="", encoding="utf-8-sig") as movie_file:
        reader = csv.reader(movie_file)
        next(reader, None)
        for row in reader:
            movies[(row[1], row[2])] = row[3]
    return movies


def read_casts(filename: str) -> dict:
    """Index the headerless cast file by (title, year)."""
    casts = {}
    with open(filename, "r", newline="", encoding="utf-8-sig") as cast_file:
        for row in csv.reader(cast_file):
            casts[(row[0], row[1])] = (row[2], row[3:])
    return casts


def ranked_totals(totals: dict) -> list:
    """Return (total, key) entries with the largest totals first."""
    ranking = []
    for key in totals:
        ranking.append((totals[key], key))
    ranking.sort(reverse=True)
    return ranking


def display_top_collaborations(limit: int = 0) -> None:
    """Display director/actor counts for rated movies; zero means all entries."""
    movies = read_movies(rated_filename)
    casts = read_casts(casts_filename)
    totals = {}
    shown = 0

    # Include the year in the key so remakes are not counted as the same movie.
    for movie in movies:
        if movie in casts:
            director, actors = casts[movie]
            counted_actors = []
            for actor in actors:
                if actor != "" and actor not in counted_actors:
                    key = (director, actor)
                    totals[key] = totals.get(key, 0) + 1
                    counted_actors.append(actor)
    print("Director / actor / top-rated movies")
    for total, key in ranked_totals(totals):
        if limit > 0 and shown >= limit:
            break
        shown = shown + 1
        print(shown, (key[0], key[1], total))


def display_top_actors(limit: int = 0) -> None:
    """Display actor box-office totals; zero means all entries."""
    movies = read_movies(grossing_filename)
    casts = read_casts(casts_filename)
    totals = {}
    shown = 0

    for movie in movies:
        if movie in casts:
            counted_actors = []
            for actor in casts[movie][1]:
                if actor != "" and actor not in counted_actors:
                    totals[actor] = totals.get(actor, 0) + int(movies[movie])
                    counted_actors.append(actor)
    print("Actor / total USA box office")
    for total, actor in ranked_totals(totals):
        if limit > 0 and shown >= limit:
            break
        shown = shown + 1
        print("{}. {}: ${:,}".format(shown, actor, total))


def main() -> None:
    """Display ten entries from each ranking using the provided CSV files."""
    print(student_name)
    print("[STATUS] Calculating movie rankings...")
    display_top_collaborations(display_limit)
    print()
    display_top_actors(display_limit)


if __name__ == "__main__":
    main()
