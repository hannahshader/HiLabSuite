from typing import Any, Dict, List
from data_structures.marker_utterance_dict import MarkerUtteranceDict
import copy
from pydantic import BaseModel

from algorithms.init import get_dependencies
from algorithms.gap import GapPlugin as gap
from algorithms.overlap import OverlapPlugin as overlap
from algorithms.pause import PausePlugin as pause
from algorithms.syllab_rate import SyllableRatePlugin as syllab_rate
from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar


class StructureInteract:
    def __init__(self, data_structure_arg):
        self.data_structure = data_structure_arg

    def interact_insert_marker(self, key: Any, value: Any):
        self.data_structure.insert_marker(self.data_structure, key, value)

    def interact_get_next_item(self, key):
        return self.data_structure.insert_marker(self.data_structure, key)

    ##get function list
    def function_list(self):
        dependencies = get_dependencies()
        applied_plugin_names = [
            dependency["plugin_name"] for dependency in dependencies
        ]
        if "overlaps" in applied_plugin_names:
            result += overlap.add_overlap_marker
        if "pauses" in applied_plugin_names:
            result += pause.add_pause_marker
        if "gaps" in applied_plugin_names:
            result += gap.add_gap_marker
        if "syllable_rate" in applied_plugin_names:
            result += syllab_rate.add_syllab_marker
        return result

    def apply_functions(self):
        apply_functions = self.function_list(self)
        self.data_structure.apply(self.data_structure, apply_functions)
