#!/usr/bin/env python
"""Fit."""
import os
import re
from pathlib import Path
from tempfile import gettempdir

from typing import Tuple, Union

from data import TOLERANCE_GRADES
from errors import FitError

TOLERANCE_INDEXES = '|'.join(TOLERANCE_GRADES)
HOLE_POSITIONS = 'A|B|C|CD|D|E|EF|F|FG|G|H|J|Js|K|M|N|P|R|S|T|U|V|X|Y|Z|ZA|ZB|ZC'
SHAFT_POSITIONS = 'a|b|c|cd|d|e|ef|f|fg|g|h|j|js|k|m|n|p|r|s|t|u|v|x|y|z|z|za|zb|zc'
LALIGN = 20
RALIGN = 5

# These values are to be calculated
Ds = 70
Di = 20
ds = -10
di = -30
margin = 5
width = 50
x_axis = 130


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

    def determine_baseline_y_position(self) -> Tuple[int, int, int]:
        margin = 10

        if Ds > 0:
            if Ds > ds:
                y_coord = margin + Ds
                y_shaft = margin
                y_axis = y_coord - ds
            else:
                y_coord = margin + ds
                y_shaft = y_coord + Ds
                y_axis = margin
        else:
            if Ds > ds:
                y_coord = margin
                y_shaft = y_coord - Ds
                y_axis =  y_coord - ds
            else:
                if ds > 0:
                    y_coord = margin + ds
                    y_shaft = y_coord - Ds
                    y_axis = margin
                else:
                    y_coord = margin
                    y_shaft = y_coord - Ds
                    y_axis = y_coord + ds

        return y_coord, y_shaft, y_axis

    def plot(self, folder: Union[None, Path], filetype: str) -> None:
        if filetype == 'svg':
            extension = 'xml'

        if folder is None:
            ofile = Path(os.path.join(gettempdir(), f"{self.value}.{extension}"))
        else:
            ofile = Path(os.path.join(folder, f"{self.value}.{extension}"))

        # Create folder
        ofile.parent.mkdir(parents=True, exist_ok=True)

        y_coord, y_shaft, y_axis = self.determine_baseline_y_position()

        if filetype == 'svg':
            data = f"""
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg">
                <!-- SHAFT -->
                <rect x="{margin}" y="{y_shaft}" width="{width}" height="{y_shaft + (Ds - Di)}"/>
                <!-- AXIS -->
                <rect x="{x_axis}" y="{y_axis}" width="{width}" height="{y_axis + (ds - di)}"/>
                <!-- BASELINE -->
                <line x1="{margin}" y1="{y_coord}" x2="{x_axis + width}" y2="{y_coord}" style="stroke:rgb(0,0,0);stroke-width:2"/>
            </svg>
            """
        else:
            data = ""

        # Create file
        ofile.write_text(data, encoding='utf-8')
