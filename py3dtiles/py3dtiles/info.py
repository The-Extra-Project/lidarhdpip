import argparse
from pathlib import Path
from typing import Any

from py3dtiles.tileset.content import read_binary_tile_content


def main(args: argparse.Namespace) -> None:
    try:
        tile_content = read_binary_tile_content(args.file)
    except ValueError as e:
        print(f"Error when reading the file {args.file}")
        raise e

    tile_content.print_info()


def init_parser(
    subparser: "argparse._SubParsersAction[Any]",
) -> argparse.ArgumentParser:
    # arg parse
    parser: argparse.ArgumentParser = subparser.add_parser(
        "info", help="Extract information from a 3DTiles file"
    )

    parser.add_argument("file", type=Path)

    return parser
