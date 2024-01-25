#!/usr/bin/env python
"""Parser."""

import argparse
import os
from enum import Enum
from pathlib import Path

from fit import Fit


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
        help="Fitting value"
    )
    parser_plot.add_argument(
        "--out",
        type=Path,
        help="Output file folder"
    )
    parser_plot.add_argument(
        "--type",
        default="svg",
        nargs="?",
        choices=["svg"],
        help="File type"
    )

    args = parser.parse_args()
    return args


def main(params):
    try:
        if params.fitting:
            fit = Fit(params.fitting)
            fit.plot(params.out, params.type)

    except AttributeError:
        raise


if __name__ == "__main__":
    params = parse_args()
    main(params)
