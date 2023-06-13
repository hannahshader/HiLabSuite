from typing import Any, Dict, List
from data_structures.init_utterance_dict import InitUtteranceDict
import copy
from pydantic import BaseModel

from algorithms.init import get_dependencies
from algorithms.gap import GapPlugin as gap
from algorithms.overlap import OverlapPlugin as overlap
from algorithms.pause import PausePlugin as pause
from algorithms.syllab_rate import SyllableRatePlugin as syllab_rate
from collections import OrderedDict


class MarkerUtteranceDict:
    def __init__(self, utterance_map_obj: InitUtteranceDict):
        ##now we have a deep copy we can add markers to
        self.map = copy.deepcopy(utterance_map_obj.utterance_map)

    def insert_marker(self, key: Any, value: Any):
        self.map[key] = value
        for key in self.map:
            self.map[key] = sorted(self.map[key], key=lambda x: x.start)

    def get_next_item(self, key):
        if key in self.map:
            current_index = self.map.index(key)
        if current_index + 1 < len(self.data):
            next_key = self.map[current_index + 1]
            next_value = self.map[next_key]
            return next_key, next_value
        return None, None

    def apply(self, apply_functions):
        for key, value in self.map.items():
            for func in apply_functions:
                curr = value
                curr_next_key, curr_next_value = self.get_next_item(self, key)
                func(curr, curr_next_value)
