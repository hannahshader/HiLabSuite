# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Hannah Shader
# @Last Modified time: 2023-07-11 16:49:41
# @Description: Creates a marker utterance dictionary

import copy
import bisect
import pickle
import sys
import threading
import itertools
from typing import Any, Dict, List, IO
from collections import OrderedDict

from Plugin_Development.src.configs.configs import INTERNAL_MARKER
from Plugin_Development.src.data_structures.data_objects import UttObj
from Plugin_Development.src.data_structures.pickling import Pickling


import copy
import os
from typing import Any, Dict, List
from typing import OrderedDict as OrderedDictType, TypeVar
from pydantic import BaseModel
from collections import OrderedDict

from Plugin_Development.src.data_structures.data_objects import UttObj
from Plugin_Development.src.algorithms.apply_plugins import ApplyPlugins
from Plugin_Development.src.configs.configs import INTERNAL_MARKER
from Plugin_Development.src.configs.configs import THRESHOLD
from Plugin_Development.src.configs.configs import load_threshold
from gailbot import Plugin
from gailbot import GBPluginMethods

THRESHOLD = load_threshold()


class MarkerUtteranceDict:
    """
    A wrapper object for init_utterance_dict with functions to add markers
    """

    def __init__(self, utterance_map=None):
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
            ## holds data about words spoken by each speaker
            self.list = []
            ## holds data about the start and end time of sentences
            self.sentences = []
            ## holds strings for each speaker's name
            ## (used later to generate xml/chat files)
            self.speakers = []
            self.overlaps = False

            # will be populated later in overlap plugin to hold the sentences that will need to be reordered
            self.overlap_ids = []
        else:
            ## intialize objects to store data
            utterances = []
            sentence_data_plain = []
            self.speakers = []
            speaker = ""
            prev_utt = None

            # will be populated later in overlap plugin to hold the sentences that will need to be reordered
            self.overlap_ids = []

            # create a counter for ids to assign to flexible info field for
            # overlapping data in folders
            # this info will take the place of speaker ids when printing the files
            # must be -1 becuase incriments up every first loop as speaker will never be ""
            counter_sentence_overlaps = -1

            # create a boolean that stores whether or not there's a folder for overlaps
            # create a variable that creates different speaker ids for each file if there are overlaps
            self.overlaps = len(utterance_map) > 1

            speaker_counter = 0

            # loop through files provided by Gailbot
            for key, value in utterance_map.items():
                # loops through each word in each file
                for utt_dict in value:
                    if (utt_dict.speaker != speaker) or (
                        self.overlaps == True
                        and self.turn_criteria_overlaps(utt_dict, prev_utt)
                    ):
                        counter_sentence_overlaps += 1

                        # populate list of speakers
                        if (
                            self.overlaps == False
                            and utt_dict.speaker not in self.speakers
                        ):
                            self.speakers.append(utt_dict.speaker)
                        elif (
                            self.overlaps == True
                            and str(speaker_counter) not in self.speakers
                        ):
                            self.speakers.append(str(speaker_counter))

                        # add data for each sentence start and end to
                        # temporary list of sentence data
                        if prev_utt != None:
                            sentence_data_plain.append(prev_utt.end)
                        sentence_data_plain.append(utt_dict.start)
                        speaker = utt_dict.speaker

                    # add data for each word in each file to a temporary
                    # list
                    # if the input is an overlaps folder, the speaker value
                    # gets set according to the file number
                    if self.overlaps == True:
                        utt = UttObj(
                            utt_dict.start,
                            utt_dict.end,
                            str(speaker_counter),
                            utt_dict.text,
                            counter_sentence_overlaps,
                        )
                    # else, speaker gets set with engine speaker id
                    else:
                        utt = UttObj(
                            utt_dict.start,
                            utt_dict.end,
                            utt_dict.speaker,
                            utt_dict.text,
                            counter_sentence_overlaps,
                        )
                    utterances.append(utt)
                    prev_utt = utt_dict

                ## get the end time of the sentence
                sentence_data_plain.append((value[-1]).end)

                ## reset the speaker data and prev for the next file
                speaker = ""
                prev_utt = None
                speaker_counter += 1

            ## group sentence start and end times so that each list element
            ## contains a start and end time

            sentence_data = []
            count = 0
            for i in range(0, len(sentence_data_plain), 2):
                sublist = [sentence_data_plain[i], sentence_data_plain[i + 1], count]
                sentence_data.append(sublist)
                count += 1

            # create a deep copy for the class
            self.list = copy.deepcopy(utterances)
            self.pickle.save_list_to_disk(self.list)
            self.sentences = copy.deepcopy(sentence_data)
            self.pickle.save_sentences_to_disk(self.sentences)

    # def turn_criteria_no_overlaps(self, utt_dict, speaker):
    #    return utt_dict.speaker != speaker

    def turn_criteria_overlaps(self, utt_dict, prev_utt):
        if prev_utt == None:
            return False
        return (utt_dict.start - prev_utt.end) >= THRESHOLD.TURN_END_THRESHOLD_SECS

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
            ## loops through the speaker list until a non marker item is found
            while next_index < len(self.list):
                next_utterance = self.list[next_index]
                if self.is_speaker_utt(next_utterance):
                    return next_utterance
                next_index += 1
            self.pickle.save_list_to_disk(self.list)
            return False
        else:
            self.pickle.save_list_to_disk(self.list)
            return False

    def is_speaker_utt(self, curr) -> bool:
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
        if curr.text in internal_marker_set:
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

        sorted_sentences = sorted(self.sentences, key=lambda x: x[0])
        self.sentences = sorted_sentences

        result = []
        combinations = list(itertools.combinations(self.sentences, 2))

        for combination in combinations:
            return_values = apply_function(combination[0], combination[1], self.list)
            markers_list = return_values[:4]  # gets the markers
            if return_values[-2:] != []:
                self.overlap_ids.append(
                    return_values[-2:]
                )  # gets the ids of overlapping sentences
            for marker in markers_list:
                self.insert_marker(marker)

        self.pickle.save_sentences_to_disk(self.sentences)

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

        ## deep copies the list so no infinite insertions/checks
        sentences_copy = copy.deepcopy(self.sentences)
        list_copy = copy.deepcopy(self.list)

        utt_list = []
        sentence_index = 0
        while sentence_index < len(sentences_copy):
            utt_index = 0
            while utt_index < len(list_copy) and sentence_index < len(sentences_copy):
                ## loops through sentences and utterances so that utt
                ## and sentence will be corresponding
                ## utt will be contained in the sentence that sentence
                ## variable provides data for
                sentence = sentences_copy[sentence_index]
                utt = list_copy[utt_index]
                ## accumulates all utterances in the sentence
                if sentence[0] <= utt.start and utt.end <= sentence[1]:
                    if self.is_speaker_utt(utt) != False:
                        utt_list.append(utt)
                    utt_index += 1
                ## if new sentence, call function and accumulating utterances
                ## again
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

        ## deep copies the list so no infinite insertions/checks
        copied_list = copy.deepcopy(self.list)
        for item in copied_list:
            ## only inspects non marker items of the list
            if self.is_speaker_utt(item) == False:
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
        ## sentence object holds speaker, text, start, end
        ## initialize a sentence object to hold bank fields
        self.pickle.load_list_from_disk(self.list)
        sentence_obj = [
            self.list[0].speaker,
            self.list[0].text + " ",
            self.list[0].start,
            self.list[0].end,
            self.list[0].flexible_info,
        ]

        for index in range(len(self.list)):
            if index != 0:
                if self.list[index].flexible_info != self.list[index - 1].flexible_info:
                    outfile.write(sentence_obj[1])
                    sentence_obj[0] = self.list[index].speaker
                    sentence_obj[1] = format_markers(self.list[index])
                    sentence_obj[2] = self.list[index].start
                    sentence_obj[3] = self.list[index].end
                else:
                    sentence_obj[1] += format_markers(self.list[index])
                    sentence_obj[3] = self.list[index].end
        if sentence_obj[1] != "  ":
            outfile.write(sentence_obj[1])
        self.pickle.save_list_to_disk(self.list)

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
        self.pickle.load_list_from_disk(self.list)

        sentence_obj = [
            self.list[0].speaker,
            format_markers(self.list[0]),
            self.list[0].start,
            self.list[0].end,
        ]

        for index in range(len(self.list)):
            if index != 0:
                if self.list[index].flexible_info != self.list[index - 1].flexible_info:
                    print_func(sentence_obj)
                    sentence_obj[0] = self.list[index].speaker
                    sentence_obj[1] = format_markers(self.list[index])
                    sentence_obj[2] = self.list[index].start
                    sentence_obj[3] = self.list[index].end
                else:
                    sentence_obj[1] += format_markers(self.list[index])
                    sentence_obj[3] = self.list[index].end

        if sentence_obj[1] != "  ":
            print_func(sentence_obj)

        self.pickle.save_list_to_disk(self.list)

    ## iterates through the list data structure creating the xml file,
    ## which will later be used to generate the chat file
    def print_all_rows_xml(
        self, apply_subelement_root, apply_subelement_word, apply_sentence_end
    ):
        self.pickle.load_list_from_disk(self.list)
        prev_speaker = ""
        sentence = apply_subelement_root(self.list[0].speaker)
        apply_subelement_word(sentence, self.list[0])

        sentence_start = 0
        sentence_end = 0

        for index in range(len(self.list)):
            if index != 0:
                if self.list[index].flexible_info != self.list[index - 1].flexible_info:
                    apply_sentence_end(sentence, sentence_start, sentence_end)
                    sentence = apply_subelement_root(self.list[index].speaker)
                    apply_subelement_word(sentence, self.list[index])
                else:
                    apply_subelement_word(sentence, self.list[index])
            sentence_end = self.list[index].end
        apply_sentence_end(sentence, sentence_start, sentence_end)
        self.pickle.save_list_to_disk(self.list)

    def order_overlap(self):
        self.pickle.load_list_from_disk(self.list)

        first_sentence_overlap_id = None
        second_sentence_overlap_id = None

        for overlap_id_pair in self.overlap_ids:
            first_sentence_overlap_id = overlap_id_pair[0]
            second_sentence_overlap_id = overlap_id_pair[1]
            self.order_overlapping_sentences(
                first_sentence_overlap_id, second_sentence_overlap_id
            )

        self.first_appearance = {}

        list_copy = copy.deepcopy(self.list)

        flex_info_groups = {}
        result = []

        for item in list_copy:
            if item.flexible_info not in flex_info_groups:
                flex_info_groups[item.flexible_info] = []

            flex_info_groups[item.flexible_info].append(item)

        for group in flex_info_groups.values():
            result.extend(group)

        self.list = result
        self.pickle.save_list_to_disk(self.list)

    def order_overlapping_sentences(
        self, first_sentence_overlap_id, second_sentence_overlap_id
    ):
        new_list = []
        start_time = float("inf")

        # get start time of sentences with both ids, get smaller one
        for item in self.list:
            if (
                item.flexible_info == first_sentence_overlap_id
                or item.flexible_info == second_sentence_overlap_id
            ):
                if item.start < start_time:
                    start_time = item.start
                new_list.append(item)

            unique_ids = [first_sentence_overlap_id, second_sentence_overlap_id]

            sorted_list = sorted(
                new_list,
                key=lambda obj: (
                    unique_ids.index(obj.flexible_info),
                    new_list.index(obj),
                ),
            )

            self.list = [
                item
                for item in self.list
                if (
                    item.flexible_info != first_sentence_overlap_id
                    and item.flexible_info != second_sentence_overlap_id
                )
            ]

            # Find the correct index to insert
            insert_index = None
            for index in range(len(self.list)):
                if self.list[index].start > start_time:
                    insert_index = index
                    break

            # If start_time is less than the start time of the first event, insert at the beginning
            if insert_index is None and (
                not self.list or start_time < self.list[0].start
            ):
                insert_index = 0
            # If start_time is greater than the start time of the last event, insert at the end
            elif insert_index is None and start_time >= self.list[-1].start:
                insert_index = len(self.list)

            # Insert at the calculated index (only once, and in a single place in the code)
            if insert_index is not None:
                self.list = (
                    self.list[:insert_index] + sorted_list + self.list[insert_index:]
                )

    def sort(self, list_to_sort, counter):
        if self.overlaps:
            unique_ids = []
            for obj in list_to_sort:
                if obj.flexible_info not in unique_ids:
                    unique_ids.append(obj.flexible_info)

            sorted_list = sorted(
                list_to_sort,
                key=lambda obj: (
                    unique_ids.index(obj.flexible_info),
                    list_to_sort.index(obj),
                ),
            )

        else:
            unique_speakers = []
            for obj in list_to_sort:
                if obj.speaker not in unique_speakers:
                    unique_speakers.append(obj.speaker)

            sorted_list = sorted(
                list_to_sort,
                key=lambda obj: (
                    unique_speakers.index(obj.speaker),
                    list_to_sort.index(obj),
                ),
            )

        return sorted_list

    def is_marker_overlap_start(self, curr):
        return (
            curr.text == INTERNAL_MARKER.OVERLAP_FIRST_START
            or curr.text == INTERNAL_MARKER.OVERLAP_SECOND_START
        )

    def is_marker_overlap_end(self, curr):
        return (
            curr.text == INTERNAL_MARKER.OVERLAP_FIRST_END
            or curr.text == INTERNAL_MARKER.OVERLAP_SECOND_END
        )
