# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-17 15:38:57
# @Description: Creates a marker utterance dictionary

import copy
import bisect
import sys
import threading
import os
import itertools
from pydantic import BaseModel
from collections import OrderedDict
from typing import Any, Dict, List, IO, Tuple
from typing import OrderedDict as OrderedDictType, TypeVar

from HiLabSuite.src.data_structures.data_objects import UttObj
from HiLabSuite.src.algorithms.apply_plugins import ApplyPlugins
from HiLabSuite.src.configs.configs import INTERNAL_MARKER
from HiLabSuite.src.configs.configs import THRESHOLD
from HiLabSuite.src.configs.configs import load_threshold

from gailbot import Plugin
from gailbot import GBPluginMethods

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################

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
        if utterance_map is None:
            # Holds data about words spoken by each speaker
            self.list = []
            # Holds data about the start and end time of sentences
            self.sentences = []
            # Holds strings for each speaker's name
            # (used later to generate xml/chat files)
            self.speakers = []
            self.overlaps = False

            # Will be populated later in overlap plugin to hold the sentences 
            # that will need to be reordered
            self.overlap_ids = []
        else:
            # Initialize objects to store data
            utterances = []
            sentence_data_plain = []
            self.speakers = []
            speaker = ""
            prev_utt = None

            # Will be populated later in overlap plugin to hold the sentences 
            # that will need to be reordered
            self.overlap_ids = []

            # Create a counter for ids to assign to flexible info field for
            # verlapping data in folders
            # This info will take the place of speaker ids when printing the 
            # files
            # Must be -1 becuase incriments up every first loop as speaker will 
            # never be ""
            counter_sentence_overlaps = -1

            # Create a boolean that stores whether or not there's a folder for
            # overlaps
            # Create a variable that creates different speaker ids for each 
            # file if there are overlaps
            self.overlaps = len(utterance_map) > 1

            speaker_counter = 0

            # Loop through files provided by Gailbot
            for key, value in utterance_map.items():
                # Loops through each word in each file
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

                        # Add data for each sentence start and end to
                        # temporary list of sentence data
                        if prev_utt != None:
                            sentence_data_plain.append(prev_utt.end)
                        sentence_data_plain.append(utt_dict.start)
                        speaker = utt_dict.speaker

                    # Add data for each word in each file to a temporary list
                    # If the input is an overlaps folder, the speaker value
                    # gets set according to the file number
                    if self.overlaps == True:
                        utt = UttObj(
                            utt_dict.start,
                            utt_dict.end,
                            str(speaker_counter),
                            utt_dict.text,
                            counter_sentence_overlaps,
                        )
                    # Else, speaker gets set with engine speaker id
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

                # Get the end time of the sentence
                sentence_data_plain.append((value[-1]).end)

                # Reset the speaker data and prev for the next file
                speaker = ""
                prev_utt = None
                speaker_counter += 1

            # Group sentence start and end times so that each list element
            # Contains a start and end time

            sentence_data = []
            count = 0
            for i in range(0, len(sentence_data_plain), 2):
                sublist = [sentence_data_plain[i], sentence_data_plain[i + 1], count]
                sentence_data.append(sublist)
                count += 1

            # Create a deep copy for the class
            self.list = copy.deepcopy(utterances)
            self.sentences = copy.deepcopy(sentence_data)


    def testing_print(self):
        """
        Testing function that prints a given output
        """
        with self.lock:
            for item in self.list:
                print(item.text)

    def turn_criteria_overlaps(self, utt_dict: dict[UttObj], prev_utt: UttObj) -> bool:
        """
        Returns whether or not the difference between two utterances meets the 
        threshold

        Parameters
        ----------
        utt_dict: the utterance dictionary
        prev_utt: the previous utterance
        
        Returns
        -------
        a boolean

        """
        if prev_utt == None:
            return False
        return (utt_dict.start - prev_utt.end) >= load_threshold().TURN_END_THRESHOLD_SECS

    def sort_list(self) -> None:
        """
        Sorts the list by start times.
        Integrates all words from each file into the main data structure

        Returns
        -------
        None

        """
        # with self.lock:
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
        # with self.lock:
        if value == None:
            return
        index = bisect.bisect_left([obj.start for obj in self.list], value.start)
        self.list.insert(index, value)

    def get_next_utt(self, current_item: UttObj) -> Any:
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
        # with self.lock:
        if current_item in self.list:
            current_index = self.list.index(current_item)
            next_index = current_index + 1
            # Loops through the speaker list until a non marker item is found
            while next_index < len(self.list):
                next_utterance = self.list[next_index]
                if self.is_speaker_utt(next_utterance):
                    return next_utterance
                next_index += 1
            return False
        else:
            return False

    def is_speaker_utt(self, curr: UttObj) -> bool:
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

    def apply_functions(self, apply_functions: List[callable]) -> list[any]:
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
        # with self.lock:
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        return result

    def apply_function(self, func: callable) -> list[any]:
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
        # with self.lock:
        result = []
        for item in self.list:
            result.append(func(item))
        return result

    def apply_for_overlap(self, apply_function: callable) -> None:
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

        sorted_sentences = sorted(self.sentences, key=lambda x: x[0])
        self.sentences = sorted_sentences

        result = []
        combinations = list(itertools.combinations(self.sentences, 2))

        for combination in combinations:
            return_values = apply_function(combination[0], combination[1], self.list)
            to_insert_list = return_values[:-2]  # gets the markers
            if return_values[-2:] != []:
                self.overlap_ids.append(
                    return_values[-2:]
                )  # Gets the ids of overlapping sentences
                for marker in to_insert_list:
                    # Get a unique id for the overlap
                    marker.overlap_id = len(self.overlap_ids)
                    self.insert_marker(marker)

    def apply_for_syllab_rate(self, func: callable) -> None:
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
        # with self.lock:

        # Deep copies the list so no infinite insertions/checks
        sentences_copy = copy.deepcopy(self.sentences)
        list_copy = copy.deepcopy(self.list)

        utt_list = []
        sentence_index = 0
        while sentence_index < len(sentences_copy):
            utt_index = 0
            while utt_index < len(list_copy) and sentence_index < len(sentences_copy):
                # Loops through sentences and utterances so that utt
                # and sentence will be corresponding
                # Utt will be contained in the sentence that sentence
                # variable provides data for
                sentence = sentences_copy[sentence_index]
                utt = list_copy[utt_index]
                # Accumulates all utterances in the sentence
                if sentence[0] <= utt.start and utt.end <= sentence[1]:
                    if self.is_speaker_utt(utt) != False:
                        utt_list.append(utt)
                    utt_index += 1
                # If new sentence, call function and accumulating utterances
                # again
                else:
                    func(utt_list, sentence[0], sentence[1])
                    utt_list = []
                    sentence_index += 1
            sentence_index += 1


    def apply_insert_marker(self, apply_functions: List[callable]) -> None:
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

        # Deep copies the list so no infinite insertions/checks
        copied_list = copy.deepcopy(self.list)
        for item in copied_list:
            # Only inspects non marker items of the list
            if self.is_speaker_utt(item) == False:
                continue
            # Applies each plugin function to each item
            for func in apply_functions:
                curr = item
                curr_next = self.get_next_utt(curr)
                # Returns if there is no next item
                if curr_next == False:
                    return
                # Storing markers as a list becuase the overlap function
                # Returns four markers
                marker = func(curr, curr_next)
                self.insert_marker(marker)

    def print_all_rows_text(self, format_markers: callable, outfile: IO[str], formatter) -> None:
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
        # sentence object holds speaker, text, start, end
        # initialize a sentence object to hold bank fields

        # SELF LOCK NOT NEEDED BECAUSE NO INSERTIONS/DELETIONS PAST THIS PNT?

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

    def print_all_rows_csv(self, print_func: callable, format_markers: callable) -> None:
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


    # Iterates through the list data structure creating the xml file,
    # Which will later be used to generate the chat file
    def print_all_rows_xml(
        self, apply_subelement_root: callable, apply_subelement_word: callable, 
        apply_sentence_end: callable
    ):
        """
        Creates the xml output for Gailbot, separating each line by its speaker

        Parameters
        ----------
        apply_subelement_root: the root function to be applied
        apply_subelement_word: the word function to be applied
        apply_subelement_word: the sentence end function to be applied

        Returns
        -------
        none
        """
        prev_speaker = ""
        sentence = apply_subelement_root(self.list[0].speaker)
        apply_subelement_word(sentence, self.list[0])

        sentence_start = 0
        sentence_end = 0

        for index in range(len(self.list)):
            if index != 0:
                if self.list[index].flexible_info != self.list[index - 1].flexible_info:
                    apply_sentence_end(sentence, sentence_start, sentence_end)
                    sentence_start = self.list[index].start
                    sentence = apply_subelement_root(self.list[index].speaker)
                    apply_subelement_word(sentence, self.list[index])
                else:
                    apply_subelement_word(sentence, self.list[index])
            sentence_end = self.list[index].end
        apply_sentence_end(sentence, sentence_start, sentence_end)

    def order_overlap(self):
        """
        Reorders the list based on the overlap specifications

        Parameters
        ----------
        none

        Returns
        -------
        none
        """
        # with self.lock:

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

    def order_overlapping_sentences(
        self, first_sentence_overlap_id: int, second_sentence_overlap_id: int
    ) -> None:
        """
        Reorders sentences based on the overlap specifications

        Parameters
        ----------
        first_sentence_overlap_id: the first sentence to reorder
        second_sentence_overlap_id: the second sentence to reorder

        Returns
        -------
        none
        """
        # with self.lock:
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

            self.insert_small_list(start_time, sorted_list)

    def insert_small_list(self, start_time: int, small_list: List[UttObj]):
        """
        Finds the correct index to insert

        Parameters
        ----------
        start_time: an integer for the start time to insert for
        small_list: the smaller list to insert the index inside of

        Returns
        -------
        none
        """
        
        insert_index = None
        for index in range(len(self.list)):
            if self.list[index].start > start_time:
                insert_index = index
                break

        # If start_time is less than the start time of the first event, insert at the beginning
        if insert_index is None and (not self.list or start_time < self.list[0].start):
            insert_index = 0
        # If start_time is greater than the start time of the last event, insert at the end
        elif insert_index is None and start_time >= self.list[-1].start:
            insert_index = len(self.list)

        # Insert at the calculated index (only once, and in a single place in the code)
        if insert_index is not None:
            self.list = self.list[:insert_index] + small_list + self.list[insert_index:]

    # gets the word before the overlap marker and checks to see if it needs to
    # be broken up
    # if so, calls the split utterance function
    def insert_overlap_markers_character_level(self):
        """
        Continue checking for overlaps not placed within utterances
        until a full loop has been completed and no utterance has
        been modified

        Parameters
        ----------
        none

        Returns
        -------
        none
        """
        # print("self.list is: ")
        # for item in self.list:
        #    print("utt is: " + str(item))
        # this list will hold smaller lists of two elements
        # [start_time, ]

        
        while True:
            old_list = self.list.copy()
            new_list = []
            i = 0
            new_insertion = False
            while i < len(old_list) - 1:
                current_item = self.list[i]
                next_item = self.list[i + 1]


                # case for passing if there are empty markers
                # TODO: make sure we're never adding empty markers?
                if (
                    next_item.text == INTERNAL_MARKER.OVERLAP_FIRST_START
                    or next_item.text == INTERNAL_MARKER.OVERLAP_FIRST_END
                    or next_item.text == INTERNAL_MARKER.OVERLAP_SECOND_START
                    or next_item.text == INTERNAL_MARKER.OVERLAP_SECOND_END
                ) and (current_item.flexible_info == next_item.flexible_info):
                    if next_item.start < current_item.end:
                        # print("curr item is: " + str(current_item))
                        # print("next item is: " + str(next_item))
                        # split the utt
                        utt_head, utt_butt = self.split_utt(current_item, next_item)

                        # insert new split utt and marker into the list
                        new_list.append(utt_head)
                        new_list.append(next_item)
                        new_list.append(utt_butt)

                        # get the index past the overlap marker
                        i += 1
                        new_insertion = True
                else:
                    if current_item.text != "":
                        new_list.append(current_item)

                i += 1

            # set self.list to the new_list
            self.list = new_list

            if old_list == self.list:
                break

    def split_utt(self, utt: UttObj , next_utt: UttObj) -> Tuple[UttObj, UttObj]:
        """
        splits an utterance based on where an overlap marker lands

        Parameters
        ----------
        utt: the curent utterance
        next_utt: the next utterance

        Returns
        -------
        none
        """
        time_elapsed = utt.end - utt.start
        number_chars = len(utt.text)
        time_per_char = time_elapsed / number_chars
        print("time_elapsed is: " + str(time_per_char))
        print("number_char is: " + str(number_chars))
        print("char start is: " + str(utt.start))
        print("char end is: " + str(utt.end))

        curr_start = utt.start
        utt_head = UttObj(utt.start, 0, utt.speaker, "", utt.flexible_info)
        utt_butt = UttObj(0, utt.end, utt.speaker, "", utt.flexible_info)

        char_list = []
        char_dict = {}
        i = 0
        print("number chars is " + str(number_chars))
        print("utt text is " + utt.text)
        while i < number_chars:
            char_dict = {}
            char_dict[utt.text[i]] = [curr_start, curr_start + time_per_char]
            char_list.append(char_dict)
            curr_start += time_per_char
            i += 1

        utt_head_list = []
        utt_butt_list = []

        for dictionary in char_list:
            start_time = list(dictionary.values())[0][0]
            if start_time > next_utt.start:
                utt_butt_list.append(dictionary)
            else:
                utt_head_list.append(dictionary)

        print("utt head list is:" + str(utt_head_list))
        print("utt butt list is:" + str(utt_butt_list))

        print("char list is:")
        for item in char_list:
            print(item)

        # if utt.text == "ffffff":
        #    print("utt is: " + str(utt))
        #    print("next utt is" + str(next_utt))
        #    print("char dict is: " + str(char_dict))

        # print("utt.text is: " + str(utt.text))
        # print("utt number_chars is: " + str(number_chars))
        # print("next utt is: " + str(next_utt))
        # print("utt is: " + str(utt))
        # print("utt head is: " + str(utt_head))
        # print("utt butt is: " + str(utt_butt))

        for i in range(number_chars):
            if curr_start < next_utt.start:
                utt_head.text += utt.text[i]
                curr_start += time_per_char
                utt_head.end = curr_start
            else:
                utt_butt.text += utt.text[i]
                utt_butt.start = curr_start
                curr_start += time_per_char

            # print("char is: " + str(utt.text[i]) + " start is: " + str(curr_start))

        # print("utt head is: " + str(utt_head))
        # print("utt butt is: " + str(utt_butt))

        return utt_head, utt_butt
