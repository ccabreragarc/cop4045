# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Number source lines and extract Python function definitions

import ast
import io
import os
import tokenize

student_name = "Cesar Cabrera Garcia"
source_filename = os.path.abspath(__file__)
numbered_filename = source_filename + ".txt"


def line_number(input_filename: str, output_filename: str) -> None:
    """Write a numbered copy of a text file; report and re-raise file errors."""
    line_counter = 1
    source_lines = []

    try:
        # Check aliases too, because opening the source for writing destroys it.
        if os.path.realpath(input_filename) == os.path.realpath(output_filename):
            raise ValueError("The input and output files must be different.")
        if os.path.exists(output_filename):
            if os.path.samefile(input_filename, output_filename):
                raise ValueError("The output points to the input file.")
        with open(input_filename, "r", encoding="utf-8") as source_file:
            source_lines = source_file.readlines()
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for current_line in source_lines:
                output_file.write(str(line_counter) + ". " + current_line)
                line_counter = line_counter + 1
    except (OSError, UnicodeError, ValueError) as error:
        print("[ERROR] Could not create the numbered file:", error)
        raise


def parse_functions(filename: str) -> tuple:
    """Return (line, name, arguments, code) records sorted by function name.

    Include nested functions. Preserve docstrings and literal string contents,
    but remove comments and blank lines outside multiline string literals.
    File and syntax errors are reported and re-raised.
    """
    source_text = ""
    function_records = []
    sorted_records = []

    try:
        with open(filename, "r", encoding="utf-8") as source_file:
            source_text = source_file.read()
        syntax_tree = ast.parse(source_text, filename=filename)
        for node in ast.walk(syntax_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_text = ast.get_source_segment(source_text, node)
                function_lines = function_text.splitlines(keepends=True)
                protected_lines = []
                tokens = list(tokenize.generate_tokens(io.StringIO(function_text).readline))
                argument_start = None
                argument_end = None
                parenthesis_depth = 0

                # Tokens distinguish real comments from a '#' inside a string.
                for token in tokens:
                    if token.type == tokenize.COMMENT:
                        row, column = token.start
                        function_lines[row - 1] = function_lines[row - 1][:column] + "\n"
                    if token.type == tokenize.STRING:
                        for row in range(token.start[0], token.end[0] + 1):
                            protected_lines.append(row)
                    if token.type == tokenize.OP and argument_end is None:
                        if token.string == "(":
                            if argument_start is None:
                                argument_start = token.end
                            parenthesis_depth = parenthesis_depth + 1
                        elif token.string == ")":
                            parenthesis_depth = parenthesis_depth - 1
                            if parenthesis_depth == 0 and argument_start is not None:
                                argument_end = token.start

                original_lines = function_text.splitlines(keepends=True)
                start_row, start_column = argument_start
                end_row, end_column = argument_end
                if start_row == end_row:
                    arguments = original_lines[start_row - 1][start_column:end_column]
                else:
                    arguments = original_lines[start_row - 1][start_column:]
                    for row in range(start_row, end_row - 1):
                        arguments = arguments + original_lines[row]
                    arguments = arguments + original_lines[end_row - 1][:end_column]

                cleaned_code = ""
                for index in range(len(function_lines)):
                    current_line = function_lines[index]
                    if current_line.strip() != "" or index + 1 in protected_lines:
                        cleaned_code = cleaned_code + current_line
                if not cleaned_code.endswith("\n"):
                    cleaned_code = cleaned_code + "\n"
                function_records.append((node.name, node.lineno, arguments, cleaned_code))

        function_records.sort()
        for record in function_records:
            sorted_records.append((record[1], record[0], record[2], record[3]))
        return tuple(sorted_records)
    except (OSError, UnicodeError, SyntaxError, tokenize.TokenError) as error:
        print("[ERROR] Could not parse the Python file:", error)
        raise


def main() -> None:
    """Test both operations on this script without overwriting the source."""
    print(student_name)
    print("[STATUS] Creating numbered source...")
    line_number(source_filename, numbered_filename)
    print("Numbered file:", numbered_filename)
    with open(numbered_filename, "r", encoding="utf-8") as numbered_file:
        for line_index in range(8):
            print(numbered_file.readline(), end="")
    print("[STATUS] Parsing functions...")
    print(parse_functions(source_filename))


if __name__ == "__main__":
    main()
