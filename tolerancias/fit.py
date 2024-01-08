#!/usr/bin/env python
"""Fit."""
import re

from .data import TOLERANCE_GRADES
from .errors import FitError

TOLERANCE_INDEXES = '|'.join(TOLERANCE_GRADES)
HOLE_POSITIONS = 'A|B|C|CD|D|E|EF|F|FG|G|H|J|Js|K|M|N|P|R|S|T|U|V|X|Y|Z|ZA|ZB|ZC'
SHAFT_POSITIONS = 'a|b|c|cd|d|e|ef|f|fg|g|h|j|js|k|m|n|p|r|s|t|u|v|x|y|z|z|za|zb|zc'


class Fit:

    def __init__(self, value: str) -> None:
        self.value = value
        self._validate()

    def _validate(self) -> None:
        regex = r'(?P<diameter>\d+)' \
            '(?P<hole_position>' + HOLE_POSITIONS + '+)' \
            '(?P<hole_tolerance>' + TOLERANCE_INDEXES + '+)' \
            '(?P<shaft_position>' + SHAFT_POSITIONS + '+)' \
            '(?P<shaft_tolerance>' + TOLERANCE_INDEXES + '+)'
        pattern = re.compile(regex)
        data = pattern.match(self.value)
        try:
            values = data.groupdict()
        except AttributeError:
            raise FitError(f"Fit value '{self.value}' does not match regex '{regex}'")
