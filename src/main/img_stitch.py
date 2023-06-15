import sys
import os
from typing import List
import argparse

__description__ = "Takes in a directory of pigeon_flight generated images "
"and a directory of csv files for each image with drone telemetry data."
"Generates a georeferenced .tif file"

def _parse_args(args: List[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--images", type=os.PathLike, required=True)
    parser.add_argument("--data", type=os.PathLike, required=True)
    return parser.parse_args(args)

def main(cmd_args: List[str]) -> None:
    args = _parse_args(cmd_args)


if __name__ == "__main__":
    main(sys.argv[1:])