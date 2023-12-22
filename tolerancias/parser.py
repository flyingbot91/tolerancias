#!/usr/bin/env python
"""Parser."""

import argparse
import re
from enum import Enum


class Action(Enum):
    """Tool actions."""

    PLOT = "plot"


def parse_args():
    """Create argument parser."""
    parser = argparse.ArgumentParser(prog="tolerancias")
    subparsers = parser.add_subparsers(help="Sub command help")

    # Plot parser
    parser_plot = subparsers.add_parser(
        Action.PLOT.value,
        help="Plot"
    )
    parser_plot.add_argument(
        "fitting",
        type=str,
        help="Fitting"
    )

    args = parser.parse_args()
    return args


def main(params):
    regex = re.compile(r'(?P<diameter>\d+)')
    data = regex.match(params.fitting)
    print(data.group('diameter'))


if __name__ == "__main__":
    params = parse_args()
    main(params)
