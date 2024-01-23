#!/usr/bin/env python
"""Fit."""
import os
import re
from pathlib import Path
from tempfile import gettempdir

from typing import Union

from data import TOLERANCE_GRADES
from errors import FitError

TOLERANCE_INDEXES = '|'.join(TOLERANCE_GRADES)
HOLE_POSITIONS = 'A|B|C|CD|D|E|EF|F|FG|G|H|J|Js|K|M|N|P|R|S|T|U|V|X|Y|Z|ZA|ZB|ZC'
SHAFT_POSITIONS = 'a|b|c|cd|d|e|ef|f|fg|g|h|j|js|k|m|n|p|r|s|t|u|v|x|y|z|z|za|zb|zc'
LALIGN = 20
RALIGN = 5


class Fit:

    def __init__(self, value: str) -> None:
        self.value = value
        self.values = {}
        self._validate()

    def __str__(self) -> str:
        return f"{self.value}\n" \
            f"{'Diameter:':<{LALIGN}} {self.values['diameter']:>{RALIGN}}\n" \
            f"{'Hole:':<{LALIGN}}\n" \
            f"{'  Position:':<{LALIGN}} {self.values['hole_position']:>{RALIGN}}\n" \
            f"{'  Tolerance:':<{LALIGN}} {self.values['hole_tolerance']:>{RALIGN}}\n" \
            f"{'Shaft:':<{LALIGN}}\n" \
            f"{'  Position:':<{LALIGN}} {self.values['shaft_position']:>{RALIGN}}\n" \
            f"{'  Tolerance:':<{LALIGN}} {self.values['shaft_tolerance']:>{RALIGN}}"

    def _validate(self) -> None:
        regex = r'(?P<diameter>\d+)' \
            '(?P<hole_position>' + HOLE_POSITIONS + '+)' \
            '(?P<hole_tolerance>' + TOLERANCE_INDEXES + '+)' \
            '(?P<shaft_position>' + SHAFT_POSITIONS + '+)' \
            '(?P<shaft_tolerance>' + TOLERANCE_INDEXES + '+)'
        pattern = re.compile(regex)
        data = pattern.match(self.value)
        try:
            self.values = data.groupdict()
        except AttributeError:
            raise FitError(f"Fit value '{self.value}' does not match regex '{regex}'")

    def plot(self, folder: Union[None, Path], filetype: str) -> None:
        if folder is None:
            ofile = Path(os.path.join(gettempdir(), f"{self.value}.{filetype}"))
        else:
            ofile = Path(os.path.join(folder, f"{self.value}.{filetype}"))

        # Create folder
        ofile.parent.mkdir(parents=True, exist_ok=True)

        if filetype == 'html':
            data = """
            <!DOCTYPE html>
            <html>
                <body>
                    <svg>
                        <rect x="10" y="30" width="50" height="100"/>
                        <rect x="100" y="120" width="50" height="100"/>
                        <line x1="0" y1="110" x2="160" y2="110" style="stroke:rgb(0,0,0);stroke-width:2"/>
                    </svg>
                </body>
            </html>
            """
        else:
            data = ""

        # Create file
        ofile.write_text(data, encoding='utf-8')
