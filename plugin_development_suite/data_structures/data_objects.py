from dataclasses import dataclass
import os


@dataclass
class UttObj:
    start: float
    end: float
    speaker: str
    text: str
