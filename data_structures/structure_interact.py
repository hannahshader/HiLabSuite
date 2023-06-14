from typing import Any, Dict, List
from data_structures.init_utterance_dict import InitUtteranceDict
from data_structures.marker_utterance_dict import MarkerUtteranceDict
import copy
from pydantic import BaseModel

from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar


# outermost layer, wraps around marker_utterance_obj
class StructureInteract:
    ##def __init__(self, data_structure_arg):
    ##    self.data_structure = data_structure_arg
    def __init__(self, utt_data=None):
        int_utterance_obj = InitUtteranceDict(utt_data)
        marker_utterance_obj = MarkerUtteranceDict(int_utterance_obj)
        self.data_structure = marker_utterance_obj

    def interact_insert_marker(self, item):
        self.data_structure.insert_marker(self.data_structure, item)

    # general apply function list for key and values in the data structure
    def apply(self, apply_functions):
        self.data_structure.apply(self.data_structure, apply_functions)

    # Takes an instance of structure interact, which holds a MarkerUtterance object
    # Takes a list of functions, which take two sequential utterances as parameters
    # Calls apply_insert_marker, which takes an instance of MarkerUtterance and a list of functions
    def apply_markers(self, apply_functions):
        self.data_structure.apply_insert_marker(self.data_structure, apply_functions)

    def is_utt(self, string):
        return self.data_structure.is_speaker_utt(string)
