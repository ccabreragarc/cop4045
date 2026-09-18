# Homework 2 - Cesar Cabrera Garcia

Problems 1-4 use direct, organized code and light status messages. Problem 5
uses type aliases, validation, structured errors, and a separate unittest suite.
All solution scripts use the Python standard library; no packages are needed
to run them. Python 3.10 or later is recommended for the annotations in problem 5.

## Run From the Repository Folder

```powershell
python Homework2/p1_CabreraGarcia_Cesar.py
python Homework2/p2_CabreraGarcia_Cesar.py
python Homework2/p3_CabreraGarcia_Cesar.py
python Homework2/p4_CabreraGarcia_Cesar.py
python Homework2/p5/p5_CabreraGarcia_Cesar.py Homework2/p5/observations.csv Homework2/p5/statistics.csv
python -m unittest discover -s Homework2/p5 -p '*_test.py' -v
python -m unittest discover -s Homework2/verification -v
```

Keep the three supplied IMDb CSV files and the supplied `testif.py` next to
problems 1-4. Their contents were copied unchanged. Problem 1 creates a separate
numbered `.py.txt` file. Problem 3 creates `social_network.csv` and includes the
extra-credit `test()` using the supplied helper.

## Interpretation Notes

- Homework 2 requires syntax that the original Module 1 guide restricted:
  functions, annotations, exceptions, comprehensions, dictionaries, and file I/O.
- The supplied ODG and PDF differ in their problem 1-4 policy wording. The
  technical requirements agree. This implementation follows the user's request
  to implement all five problems.
- Problem 4's `p3` filename is treated as a typo; its solution is named `p4`.
- Problem 1 uses `ast` and `tokenize` to identify functions and comments safely.
  Docstrings and blank lines inside string literals are preserved because they
  are program data. Nested functions are included; decorators are not part of
  the requested signature/body. Output retains the original argument spelling.
- Problem 2 uses the requested Cash/Linux sample names instead of the optional
  examples in the assignment. Each required result uses a comprehension.
- Social-network CSV is headerless: username, full name, then friend usernames.
  Existing friendships succeed without adding duplicate links. Self-links fail.
- Movie joins use both title and year. Display functions accept an optional
  limit; zero or a negative value displays the complete ranking. Main uses 10.
- Weather input is headerless, with one observation per physical line. Dates
  follow `HH:MM:SS AM/PM MM/DD/YYYY`, with no time-zone conversion. Valid records
  retain their date strings and are sorted chronologically using `datetime`.
- The first valid observation for each station/timestamp wins. Bad lines are
  reported and skipped. Invalid dates, NaN, and infinite temperatures are rejected.
- Weather statistics map each station to `(minimum, maximum, mean)`.
  The output CSV has `station,min,max,mean` as its header, alphabetically sorted
  station rows, and one decimal place. `write_statistics` cannot output individual
  observations because its required argument contains only station statistics.
- CLI exit codes: 0 for a completed report (including skipped invalid lines),
  1 for file errors, and 2 for usage errors or identical input/output paths.

## Document and Submission Status

The final documents are [submission/h2.pdf](submission/h2.pdf) and
[submission/h2.docx](submission/h2.docx). They contain the solutions in order,
the problem 5 tests, captured output, and all six supplied screenshots.
Placeholders and draft notes have been removed.

The `submission` folder also contains the Python solutions, tests, and required
data files. Original screenshots are in `Screenshots`. Local draft documents
and backups are not part of the submission package.

Verification: all 17 automated tests passed. The six embedded screenshots match
the supplied image files without modification. The final PDF contains 17 pages.

Upload the final PDF and required Python source files to Canvas. Canvas upload
is separate from publishing this repository to GitHub.
