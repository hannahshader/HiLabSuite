from typing import Any, Dict, List
from plugin_development_suite.data_structures.data_objects import INTERNAL_MARKER
from plugin_development_suite.data_structures.data_objects import UttObj
import pickle

import copy
from pydantic import BaseModel

from plugin_development_suite.algorithms.gap import GapPlugin as gap
from plugin_development_suite.algorithms.overlap import OverlapPlugin as overlap
from plugin_development_suite.algorithms.pause import PausePlugin as pause
from plugin_development_suite.algorithms.syllab_rate import (
    SyllableRatePlugin as syllab_rate,
)
from collections import OrderedDict
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods


# wrapper object for init_utterance_dict with functions to add marker
class MarkerUtteranceDict:
    ##called on the resulting object from get_utterance_object from gailbot
    ## return type is Dict[str, List[UttObj]]
    ##methods: GBPluginMethods

    def __init__(self, utterance_map: Dict[str, List[UttObj]] = None):
        if utterance_map is None:
            self.list = []
        else:
            ## get utterances into a list
            utterances = []
            for key, value in utterance_map.items():
                for utt_dict in value:
                    utt = UttObj(
                        utt_dict["start"],
                        utt_dict["end"],
                        utt_dict["speaker"],
                        utt_dict["text"],
                    )
                    utterances.append(utt)

            ## sort the list
            utterances = sorted(utterances, key=lambda x: x.start)

            # create a deep copy for the class
            self.list = copy.deepcopy(utterances)

    def insert_marker(self, value: Any):
        self.list.append(value)
        self.list = sorted(self.list, key=lambda x: x.start)

    def get_next_item(self, current_item):
        if current_item in self.list:
            current_index = self.list.index(current_item)
            if current_index + 1 < len(self.list):
                next_item = self.list[current_index + 1]
                return next_item
            else:
                ##error case
                return False
        else:
            ##error case
            return False

    def get_next_item(self, current_item):
        current_index = self.list.index(current_item)
        if current_index + 1 < len(self.list):
            next_item = self.list[current_index + 1]
            return next_item
        else:
            ##error case
            return False

    def get_next_utt(self, current_item):
        current_index = self.list.index(current_item)
        for item in self.list[current_index + 1]:
            if self.is_speaker_utt(item.speaker):
                return item
        return False

    def is_speaker_utt(self, string):
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        if string in internal_marker_set:
            return True
        else:
            return False

    """
    def apply(self, apply_functions):
        for item in self.list:
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_item
                ##returns if there is no next item
                if curr_next == False:
                    return
                func(curr, curr_next)
    """

    def apply(self, apply_functions):
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        return result

    ##Takes an instance of MarkerUtteranceDict, or self
    ##Takes a list of functions to apply that have arguments as two utterances
    ##These functions return either one or four marker values
    ##These marker values are added one by one to the list in MarkerUtteranceDict
    def apply_insert_marker(self, apply_functions):
        for item in self.list:
            if self.is_speaker_utt(item.speaker) == False:
                continue
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_utt
                ##returns if there is no next item
                if curr_next == False:
                    return
                ##storing markers as a list becuase the overlap function
                ##returns four markers
                markers_list = []
                markers_list.append(func(curr, curr_next))
                for marker in markers_list:
                    self.insert_marker(marker)

    """
    def store_list(list_to_store, filename):
        with open(filename, 'wb') as f:
            pickle.dump(list_to_store, f)
    """