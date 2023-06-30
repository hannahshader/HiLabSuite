# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-06-30 17:06:50
# @Description: Creates a marker utterance dictionary

import copy
import bisect
import pickle
import sys
import threading
from typing import Any, Dict, List, IO
from collections import OrderedDict

from plugin_development_suite.configs.configs import INTERNAL_MARKER
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.data_structures.pickling import Pickling
from plugin_development_suite.algorithms.apply_plugins import ApplyPlugins

from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods


import copy
import os
from typing import Any, Dict, List
from typing import OrderedDict as OrderedDictType, TypeVar
from pydantic import BaseModel
from collections import OrderedDict

from plugin_development_suite.data_structures.marker_utterance_dict import (
    MarkerUtteranceDict,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.algorithms.apply_plugins import ApplyPlugins
from plugin_development_suite.configs.configs import INTERNAL_MARKER
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods


class MarkerUtteranceDict:
    """
    A wrapper object for init_utterance_dict with functions to add markers
    """

    def __init__(
        self, utterance_map: Dict[str, List[UttObj]] = None
    ) -> Dict[str, List[UttObj]]:
        """
        Called on the resulting object from get_utterance_object from gailbot
        Return type is Dict[str, List[UttObj]]

        The underlying data structure holds two lists
        One list is the data for individual words/markers spoken: their
        speaker, their start time, their end time, and their id
        One list holds data about the start times and end times of sentences

        Parameters
        ----------
        utterance_map: a dictionary of strings and utterance objects

        Returns
        -------
        a dictionary of strings and utterance objects
        """
        self.lock = threading.Lock()
        self.pickle = Pickling()
        if utterance_map is None:
            # Holds data about words spoken by each speaker
            self.list = []
            # Holds data about the start and end time of sentences
            self.sentences = []
            # Holds strings for each speaker's name
            # (used later to generate xml/chat files)
            self.speakers = []
        else:
            # Populates the data about words spoken
            utterances = []
            sentence_data_plain = []
            self.speakers = []
            speaker = ""
            prev_utt = None

            # Loop through files provided by Gailbot
            for key, value in utterance_map.items():
                # Loops through each word in each file
                for utt_dict in value:
                    # Looks for speaker change to find end of sentence
                    if utt_dict.speaker != speaker:
                        # Populate list of speakers
                        if utt_dict.speaker not in self.speakers:
                            self.speakers.append(utt_dict.speaker)

                        # Add data for each sentence start and end to
                        # Temporary list of sentence data
                        if prev_utt != None:
                            sentence_data_plain.append(prev_utt.end)
                        sentence_data_plain.append(utt_dict.start)
                        speaker = utt_dict.speaker

                    # Add data for each word in each file to a temporary list
                    utt = UttObj(
                        utt_dict.start,
                        utt_dict.end,
                        utt_dict.speaker,
                        utt_dict.text,
                    )
                    utterances.append(utt)
                    prev_utt = utt_dict

                # Get the end time of the sentence
                sentence_data_plain.append((value[-1]).end)

                # Reset the speaker data and prev for the next file
                speaker = ""
                prev_utt = None

            # Group sentence start and end times so that each list element
            # Contains a start and end time
            sentence_data = []
            for i in range(0, len(sentence_data_plain), 2):
                sublist = [sentence_data_plain[i], sentence_data_plain[i + 1]]
                sentence_data.append(sublist)

            # Create a deep copy for the class
            self.list = copy.deepcopy(utterances)
            self.pickle.save_list_to_disk(self.list)
            self.sentences = copy.deepcopy(sentence_data)
            self.pickle.save_sentences_to_disk(self.sentences)

    def sort_list(self) -> None:
        """
        Sorts the list by start times.
        Integrates all words from each file into the main data structure

        Returns
        -------
        None

        """
        self.list = sorted(self.list, key=lambda x: x.start)

    def insert_marker(self, value: Any) -> None:
        """
        Inserts a marker into the data structure while maintaining the order

        Parameters
        ----------
        value: the marker to insert

        Returns
        -------
        none
        """
        with self.lock:
            self.pickle.load_list_from_disk(self.list)
            if value == None:
                return
            index = bisect.bisect_left([obj.start for obj in self.list], value.start)
            self.list.insert(index, value)
            self.pickle.save_list_to_disk(self.list)

    def get_next_utt(self, current_item) -> Any:
        """
        Given a current element in the list, gets the next element in the
        list that is not a marker, but is an utterance with corresponding text

        Parameters
        ----------
        current_item: the item from which to get the next following utterance

        Returns
        -------
        the next utterance
        """
        self.pickle.load_list_from_disk(self.list)
        if current_item in self.list:
            current_index = self.list.index(current_item)
            next_index = current_index + 1
            # Loops through the speaker list until a non marker item is found
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

    def is_speaker_utt(self, string) -> bool:
        """
        Checks the speaker field of piece of data to see if utterance is
        a marker

        Parameters
        ----------
        string: the string to check if it is a speaker utterance

        Returns
        -------
        a boolean of whether said string is a speaker utterance.
        """
        internal_marker_set = INTERNAL_MARKER.INTERNAL_MARKER_SET
        if string in internal_marker_set:
            return False
        else:
            return True

    def apply_functions(self, apply_functions) -> list[any]:
        """
        Gets a list of functions.
        Iterates through all items in the list and applies
        the list of functions to each item

        Parameters
        ----------
        apply_functions: the list of functions to apply

        Returns
        -------
        a list of all of the results of the functions run
        """
        self.pickle.load_list_from_disk(self.list)
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        self.pickle.save_list_to_disk(self.list)
        return result

    def apply_function(self, func) -> list[any]:
        """
        Gets a single function.
        Iterates through all items in the list and applies
        said function to each item

        Parameters
        ----------
        func: the function to run

        Returns
        -------
        a list of the result of the function run
        """
        self.pickle.load_list_from_disk(self.list)
        result = []
        for item in self.list:
            result.append(func(item))
        self.pickle.save_list_to_disk(self.list)
        return result

    def apply_for_overlap(self, apply_function) -> None:
        """
        Iterates through list of sentence data and inserts markers
        Will always be used to add overlap plugin markers

        Parameters
        ----------
        apply_function: the function to run for overlap purposes

        Returns
        -------
        none
        """
        self.pickle.load_sentences_from_disk(self.sentences)

        result = []
        for curr_item in self.sentences:
            curr_index = self.sentences.index(curr_item)
            if curr_index + 1 < len(self.sentences):
                # Gets a pair of start time and end time for each sentence
                # Uses this data to insert an overlap marker
                next_item = self.sentences[curr_index + 1]
                markers_list = apply_function(curr_item, next_item)
                for marker in markers_list:
                    self.insert_marker(marker)
                self.pickle.save_sentences_to_disk(self.sentences)
            else:
                self.pickle.save_sentences_to_disk(self.sentences)
                return

    def apply_for_syllab_rate(self, func) -> None:
        """
        Iterates through list of sentence data and inserts pairs of markers
        for the start and end of fast/slow speech

        Parameters
        ----------
        func: the function to run for syllable rate purposes

        Returns
        -------
        none
        """
        self.pickle.load_sentences_from_disk(self.sentences)
        self.pickle.load_list_from_disk(self.list)

        # Deep copies the list so no infinite insertions/checks
        sentences_copy = copy.deepcopy(self.sentences)
        list_copy = copy.deepcopy(self.list)

        utt_list = []
        sentence_index = 0
        while sentence_index < len(sentences_copy):
            utt_index = 0
            while utt_index < len(list_copy):
                # Loops through sentences and utterances so that utt
                # and sentence will be corresponding
                # utt will be contained in the sentence that sentence
                # variable provides data for
                sentence = sentences_copy[sentence_index]
                utt = list_copy[utt_index]
                # Accumulates all utterances in the sentence
                if sentence[0] <= utt.start and utt.end <= sentence[1]:
                    if self.is_speaker_utt(utt.speaker) != False:
                        utt_list.append(utt)
                    utt_index += 1
                # If new sentence, call function and accumulating utterances
                # again
                else:
                    func(utt_list, sentence[0], sentence[1])
                    utt_list = []
                    sentence_index += 1
            sentence_index += 1

        self.pickle.save_sentences_to_disk(self.sentences)
        self.pickle.save_list_to_disk(self.list)

    def apply_insert_marker(self, apply_functions) -> None:
        """
        Takes a list of functions to apply that have arguments as two utterances
        These functions return either one or four marker values
        These marker values are added one by one to the list in
        MarkerUtteranceDict

        Parameters
        ----------
        apply_functions: a list of functions to run and add their marker values
        to the list in MarkerUtteranceDict

        Returns
        -------
        none
        """
        self.pickle.load_list_from_disk(self.list)

        # Deep copies the list so no infinite insertions/checks
        copied_list = copy.deepcopy(self.list)
        for item in copied_list:
            # Only inspeaks non marker items of the list
            if self.is_speaker_utt(item.speaker) == False:
                continue
            # Applies each plugin function to each item
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_utt(curr)
                # Returns if there is no next item
                if curr_next == False:
                    self.pickle.save_list_to_disk(self.list)
                    return
                # Stores markers as a list becuase the overlap function
                # Returns four markers
                marker = func(curr, curr_next)
                self.insert_marker(marker)

        self.pickle.save_list_to_disk(self.list)

    def print_all_rows_text(self, format_markers, outfile: IO[str], formatter) -> None:
        """
        Creates the text output for Gailbot

        Parameters
        ----------
        format_markers: the function for marker formatting depending on
        the type of output
        outfile: the file to which gailbot will output
        formatter: the format of the strings to write to said outfile

        Returns
        -------
        none

        """
        # Format: speaker, text, start, end
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            # If not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                sentence_obj[1] += format_markers(self.list[index])
            else:
                # Gets the next utterance. Gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                # Checks if the next index is from a different speaker
                if next_utt == False or next_utt.speaker != self.list[index].speaker:
                    sentence_obj[3] = self.list[index].end
                    sentence_obj[1] += self.list[index].text + " "
                    sentence_obj[0] = self.list[index].speaker
                    write_string = formatter(
                        sentence_obj[0],
                        sentence_obj[1],
                        sentence_obj[2],
                        sentence_obj[3],
                    )
                    ## output fomatted string
                    outfile.write(write_string)
                    ## reset sentence object
                    sentence_obj[1] = ""
                    sentence_obj[2] = self.list[index].start
                # If we have the same speaker as the previous instances, then
                # just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker

    def print_all_rows_csv(self, print_func, format_markers) -> None:
        """
        Creates the csv output for Gailbot, separating each line by its speaker

        Parameters
        ----------
        print_func: the function for printing the csv output file
        format_markers:

        Returns
        -------
        none
        """
        # Format: speaker, text, start, end
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            # If not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                sentence_obj[1] += format_markers(self.list[index])
            else:
                # Gets the next utterance. Gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                # Checks if the next index is from a different speaker
                if next_utt == False or next_utt.speaker != self.list[index].speaker:
                    sentence_obj[3] = self.list[index].end
                    sentence_obj[1] += self.list[index].text + " "
                    sentence_obj[0] = self.list[index].speaker
                    print_func(sentence_obj)
                    sentence_obj[1] = ""
                    sentence_obj[2] = self.list[index].start
                # If we have the same speaker as the previous instances,
                # just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker
