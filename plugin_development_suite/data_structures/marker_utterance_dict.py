from typing import Any, Dict, List
from plugin_development_suite.configs.configs import INTERNAL_MARKER
from plugin_development_suite.data_structures.data_objects import UttObj

import copy
import bisect

from plugin_development_suite.algorithms.gap import GapPlugin
from plugin_development_suite.algorithms.overlap import OverlapPlugin
from plugin_development_suite.algorithms.pause import PausePlugin
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
            self.sentences = []
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

            sentence_data = []
            for key, utt_objs in utterance_map.items():
                first_start_time = float("inf")
                last_end_time = float("-inf")

                for obj in utt_objs:
                    start_time = obj["start"]
                    end_time = obj["end"]
                    if start_time < first_start_time:
                        first_start_time = start_time
                    if end_time > last_end_time:
                        last_end_time = end_time

                result = [first_start_time, last_end_time]
                sentence_data.append(result)

            # create a deep copy for the class
            self.list = copy.deepcopy(utterances)
            self.sentences = copy.deepcopy(sentence_data)

    # inserts a marker into the data structure and resorts the list
    def insert_marker(self, value: Any):
        if value == None:
            return
        index = bisect.bisect_left([obj.start for obj in self.list], value.start)
        self.list.insert(index, value)

    # given a current element in list, gets the next element in the list
    def get_next_item(self, current_item):
        if current_item in self.list:
            current_index = self.list.index(current_item)
            if current_index + 1 < len(self.list):
                next_item = self.list[current_index + 1]
                return next_item
            else:
                ##error case
                return None
        else:
            ##error case
            return None

    def get_next_sentence_item(self, current_item):
        if current_item in self.sentences:
            current_index = self.sentences.index(current_item)
            if current_index + 1 < len(self.sentences):
                next_item = self.sentences[current_index + 1]
                return next_item
            else:
                ##error case
                return None
        else:
            ##error case
            return None

    # given a current element in the list, gets the next element in the
    # list that is not a marker, but is an utterance with corresponding text
    def get_next_utt(self, current_item):
        current_index = self.list.index(current_item)
        if current_index > len(self.list):
            return False
        next_index = current_index + 1

        while next_index < len(self.list):
            next_utterance = self.list[next_index]
            if self.is_speaker_utt(next_utterance.speaker):
                return next_utterance
            next_index += 1

        return False

    ## check the speaker field of piece of data to see if utterance is a marker
    def is_speaker_utt(self, string):
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        if string in internal_marker_set:
            return False
        else:
            return True

    ## gets a list of functions
    ## iterates through all items in the list and applies
    ## the list of functions to each item
    def apply(self, apply_functions):
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        return result

    ## gets a list of functions
    ## iterates through all items in the list and applies
    ## the list of functions to each item
    def apply_for_overlap(self, apply_function):
        result = []
        for item in self.sentences:
            curr = item
            curr_next = self.get_next_sentence_item(curr)
            ##returns if there is no next item
            if curr_next == None:
                return
            markers_list = apply_function(curr, curr_next)
            for marker in markers_list:
                self.insert_marker(marker)

    ## Takes an instance of MarkerUtteranceDict, or self
    ## Takes a list of functions to apply that have arguments as two utterances
    ## These functions return either one or four marker values
    ## These marker values are added one by one to the list in MarkerUtteranceDict
    def apply_insert_marker(self, apply_functions):
        for item in self.list:
            if self.is_speaker_utt(item.speaker) == False:
                continue
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_utt(curr)
                ##returns if there is no next item
                if curr_next == False:
                    return
                ##storing markers as a list becuase the overlap function
                ##returns four markers
                marker = func(curr, curr_next)
                self.insert_marker(marker)
