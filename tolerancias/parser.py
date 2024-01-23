#!/usr/bin/env python
"""Parser."""

import argparse
import os
import re
from enum import Enum
from pathlib import Path
from tempfile import gettempdir

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
        default="html",
        nargs="?",
        choices=["html"],
        help="File type"
    )

    args = parser.parse_args()
    return args


def main(params):
    try:
        if params.fitting:
            if params.out is None:
                params.out = Path(os.path.join(gettempdir(), f"{params.fitting}.{params.type}"))

            fit = Fit(params.fitting)
            fit.plot(params.out)

    except AttributeError:
        raise


if __name__ == "__main__":
    params = parse_args()
    main(params)
