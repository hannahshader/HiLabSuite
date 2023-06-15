from typing import Any, Dict, List
from data_structures.init_utterance_dict import InitUtteranceDict
from data_structures.marker_utterance_dict import MarkerUtteranceDict
import copy
import os
from pydantic import BaseModel

from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar

## Used to be OUT_PATH = "/Users/yike/Desktop/plugin_output"
OUT_PATH = "Temporary"


# outermost layer, wraps around marker_utterance_obj
class StructureInteract:
    def __init__(self, utt_data=None, output_path=None):
        int_utterance_obj = InitUtteranceDict(utt_data)
        marker_utterance_obj = MarkerUtteranceDict(int_utterance_obj)
        self.data_structure = marker_utterance_obj

        if output_path:
            self.output = output_path
            os.makedirs(output_path, exist_ok=True)
        else:
            self.output = OUT_PATH

    def interact_insert_marker(self, item):
        self.data_structure.insert_marker(self.data_structure, item)

    # general apply function list for key and values in the data structure
    def apply(self, apply_functions):
        self.data_structure.apply(apply_functions)

    # Takes an instance of structure interact, which holds a MarkerUtterance object
    # Takes a list of functions, which take two sequential utterances as parameters
    # Calls apply_insert_marker, which takes an instance of MarkerUtterance and a list of functions
    def apply_markers(self, apply_functions):
        self.data_structure.apply_insert_marker(apply_functions)
