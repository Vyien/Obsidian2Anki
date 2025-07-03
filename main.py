import argparse
import pathlib
import sys

import src.converter as converter


def parse_arguments() -> argparse.Namespace:
    """
     Parses command-line arguments for the Obsidian2Anki converter.

    The script expects:
        - a path to the input Markdown file,
        - a name/path for the output CSV file,
        - a separator string used to distinguish questions from answers.

    Returns:
        argparse.Namespace: An object containing parsed arguments:
            - md_path (pathlib.Path): Path to the input .md file.
            - csv_name (pathlib.Path): Output CSV file name or path.
            - separator (str): String that separates questions from answers in the Markdown file.
    """
    arg_parser = argparse.ArgumentParser(
        prog="Obsidian2Anki",
        description="Converts a Markdown file with flashcard-style content into a CSV file compatible with Anki.",
    )
    arg_parser.add_argument(
        "md_path", type=pathlib.Path, help="path to .md file you want to convert"
    )
    arg_parser.add_argument(
        "csv_name", type=pathlib.Path, help="name of the output csv file"
    )
    arg_parser.add_argument(
        "separator",
        type=str,
        help="separator separating questions from answers in your md file",
    )
    return arg_parser.parse_args()


def main() -> int:
    args = parse_arguments()
    converter.parse_markdown_to_csv(args.md_path, args.csv_name, args.separator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
