from typing import Any, Dict, List
from plugin_development_suite.configs.configs import INTERNAL_MARKER
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.data_structures.pickling import Pickling

import copy
import bisect
import pickle
import sys
import threading

from collections import OrderedDict
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods


# wrapper object for init_utterance_dict with functions to add marker
class MarkerUtteranceDict:
    ##called on the resulting object from get_utterance_object from gailbot
    ## return type is Dict[str, List[UttObj]]
    ##methods: GBPluginMethods

    ## The underlying data structure holds two lists
    ## One list is the data for individual words/markers spoken: their
    ## speaker, their start time, their end time, and their id
    ## One list holds data about the start times and end times of sentences
    def __init__(self, utterance_map: Dict[str, List[UttObj]] = None):
        self.lock = threading.Lock()
        self.pickle = Pickling()
        if utterance_map is None:
            self.list = []
            self.sentences = []
        else:
            ## Populate data about words spoken
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

            # Populate data about sentences
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
            self.pickle.save_list_to_disk(self.list)
            self.sentences = copy.deepcopy(sentence_data)
            self.pickle.save_sentences_to_disk(self.sentences)

    ## inserts a marker into the data structure
    ## maintains original order
    def insert_marker(self, value: Any):
        with self.lock:
            self.pickle.load_list_from_disk(self.list)
            if value == None:
                return
            index = bisect.bisect_left([obj.start for obj in self.list], value.start)
            self.list.insert(index, value)
            self.pickle.save_list_to_disk(self.list)

    # given a current element in the list, gets the next element in the
    # list that is not a marker, but is an utterance with corresponding text
    def get_next_utt(self, current_item):
        self.pickle.load_list_from_disk(self.list)
        if current_item in self.list:
            current_index = self.list.index(current_item)
            next_index = current_index + 1
            while next_index < len(self.list):
                next_utterance = self.list[next_index]
                if self.is_speaker_utt(next_utterance.speaker):
                    return next_utterance
                next_index += 1
            self.pickle.save_list_to_disk(self.list)
            return False
        else:
            self.pickle.save_list_to_disk(self.list)
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
        self.pickle.load_list_from_disk(self.list)
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        self.pickle.save_list_to_disk(self.list)
        return result

    ## Iterates through list of sentence data
    ## Inserts markers
    ## Will always be used to add overlap plugin markers
    def apply_for_overlap(self, apply_function):
        self.pickle.load_sentences_from_disk(self.sentences)
        result = []
        for curr_item in self.sentences:
            curr_index = self.sentences.index(curr_item)
            if curr_index + 1 < len(self.sentences):
                next_item = self.sentences[curr_index + 1]
                markers_list = apply_function(curr_item, next_item)
                for marker in markers_list:
                    self.insert_marker(marker)
                self.pickle.save_sentences_to_disk(self.sentences)
            else:
                self.pickle.save_sentences_to_disk(self.sentences)
                return

    def apply_for_syllab_rate(self, func):
        self.pickle.load_sentences_from_disk(self.sentences)
        self.pickle.load_list_from_disk(self.list)
        for curr_sentence in self.sentences:
            ## using second list item, get the sentence end time
            sentence_end_time = curr_sentence[1]
            for curr_item in self.list:
                if self.is_speaker_utt(curr_item.speaker) == False:
                    continue
                elif curr_item.end <= sentence_end_time:
                    func(curr_item, curr_sentence[0], curr_sentence[1])
                    self.pickle.save_sentences_to_disk(self.sentences)
                    self.pickle.save_list_to_disk(self.list)
                else:
                    continue

    ## Takes a list of functions to apply that have arguments as two utterances
    ## These functions return either one or four marker values
    ## These marker values are added one by one to the list in MarkerUtteranceDict
    def apply_insert_marker(self, apply_functions):
        self.pickle.load_list_from_disk(self.list)

        ## deep copies the list so no infinite insertions/checks
        copied_list = copy.deepcopy(self.list)
        for item in copied_list:
            ## only inspeaks non marker items of the list
            if self.is_speaker_utt(item.speaker) == False:
                continue
            ## applies each plugin function to each item
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_utt(curr)
                ##returns if there is no next item
                if curr_next == False:
                    self.pickle.save_list_to_disk(self.list)
                    return
                ##storing markers as a list becuase the overlap function
                ##returns four markers
                marker = func(curr, curr_next)
                self.insert_marker(marker)

        self.pickle.save_list_to_disk(self.list)
