# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 14:22:48
# @Description: Creates a marker utterance dictionary

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


class MarkerUtteranceDict:
    ## The underlying data structure holds two lists
    ## One list is the data for individual words/markers spoken: their
    ## speaker, their start time, their end time, and their id
    ## One list holds data about the start times and end times of sentences
    def __init__(self, utterance_map: Dict[str, List[UttObj]] = None):
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
        else:
            ## intialize objects to store data
            utterances = []
            sentence_data_plain = []
            self.speakers = []
            speaker = ""
            prev_utt = None

            ## loop through files provided by Gailbot
            for key, value in utterance_map.items():
                ## loops through each word in each file
                for utt_dict in value:
                    ## looks for speaker change to find end of sentence
                    if utt_dict.speaker != speaker:
                        ## populate list of speakers
                        if utt_dict.speaker not in self.speakers:
                            self.speakers.append(utt_dict.speaker)

                        ## add data for each sentence start and end to
                        ## temporary list of sentence data
                        if prev_utt != None:
                            sentence_data_plain.append(prev_utt.end)
                        sentence_data_plain.append(utt_dict.start)
                        speaker = utt_dict.speaker

                    ## add data for each word in each file to a temporary
                    ## list
                    utt = UttObj(
                        utt_dict.start,
                        utt_dict.end,
                        utt_dict.speaker,
                        utt_dict.text,
                    )
                    utterances.append(utt)
                    prev_utt = utt_dict

                ## get the end time of the sentence
                sentence_data_plain.append((value[-1]).end)

                ## reset the speaker data and prev for the next file
                speaker = ""
                prev_utt = None

            ## group sentence start and end times so that each list element
            ## contains a start and end time
            sentence_data = []
            for i in range(0, len(sentence_data_plain), 2):
                sublist = [sentence_data_plain[i], sentence_data_plain[i + 1]]
                sentence_data.append(sublist)

            # create a deep copy for the class
            self.list = copy.deepcopy(utterances)
            self.pickle.save_list_to_disk(self.list)
            self.sentences = copy.deepcopy(sentence_data)
            self.pickle.save_sentences_to_disk(self.sentences)

    # sorts the list by start times
    # integrates all words from each files into the main data structure
    def sort_list(self):
        self.list = sorted(self.list, key=lambda x: x.start)

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
            ## loops through the speaker list until a non marker item is found
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
    def apply_functions(self, apply_functions):
        self.pickle.load_list_from_disk(self.list)
        result = []
        for item in self.list:
            for func in apply_functions:
                result.append(func(item))
        self.pickle.save_list_to_disk(self.list)
        return result

    ## get a single function
    ## iterates through all items in the list and applies
    ## function to each item
    def apply_function(self, func):
        self.pickle.load_list_from_disk(self.list)
        result = []
        for item in self.list:
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
                ## gets a pair of start time and end time for each sentence
                ## uses this data to insert an overlap marker
                next_item = self.sentences[curr_index + 1]
                markers_list = apply_function(curr_item, next_item)
                for marker in markers_list:
                    self.insert_marker(marker)
                self.pickle.save_sentences_to_disk(self.sentences)
            else:
                self.pickle.save_sentences_to_disk(self.sentences)
                return

    ## called in the syllable rate plugin to iterate through items in the
    ## list data structure and mark series of words that have slowspeech or
    ## fastspeech
    def apply_for_syllab_rate(self, func):
        self.pickle.load_sentences_from_disk(self.sentences)
        self.pickle.load_list_from_disk(self.list)

        ## deep copies the list so no infinite insertions/checks
        sentences_copy = copy.deepcopy(self.sentences)
        list_copy = copy.deepcopy(self.list)

        utt_list = []
        sentence_index = 0
        while sentence_index < len(sentences_copy):
            utt_index = 0
            while utt_index < len(list_copy):
                ## loops through sentences and utterances so that utt
                ## and sentence will be corresponding
                ## utt will be contained in the sentence that sentence
                ## variable provides data for
                sentence = sentences_copy[sentence_index]
                utt = list_copy[utt_index]
                ## accumulates all utterances in the sentence
                if sentence[0] <= utt.start and utt.end <= sentence[1]:
                    if self.is_speaker_utt(utt.speaker) != False:
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

    ## Takes a list of functions to apply that have arguments as two utterances
    ## These functions return either one or four marker values
    ## These marker values are added one by one to the list in MarkerUtteranceDict
    def apply_insert_marker(self, apply_functions):
        self.pickle.load_list_from_disk(self.list)

        ## deep copies the list so no infinite insertions/checks
        copied_list = copy.deepcopy(self.list)
        for item in copied_list:
            ## only inspects non marker items of the list
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

    ## iterates through the list data structure creating the text output
    ## for Gailbot
    def print_all_rows_text(self, format_markers, outfile, formatter):
        ## sentence object holds speaker, text, start, end
        ## initialize a sentence object to hold bank fields
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            ## if not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                sentence_obj[1] += format_markers(self.list[index])
            else:
                ## gets the next utterance. gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                ## if the next index is from a different speaker
                if next_utt == False or next_utt.speaker != self.list[index].speaker:
                    ## change fields of the sentence object to reflect a sentence
                    ## instead of a word
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
                ## if we have the same speaker as the previous instances
                ## just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker

    ## iterates through the list data structure creating the csv output
    ## for Gailbot, separating each line by its speaker
    def print_all_rows_csv(self, print_func, format_markers):
        ## sentence object holds speaker, text, start, end
        ## initialize a sentence object to hold bank fields
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            ## if not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                sentence_obj[1] += format_markers(self.list[index])
            else:
                ## gets the next utterance. gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                ## if the next index is from a different speaker
                if next_utt == False or next_utt.speaker != self.list[index].speaker:
                    sentence_obj[3] = self.list[index].end
                    sentence_obj[1] += self.list[index].text + " "
                    sentence_obj[0] = self.list[index].speaker
                    print_func(sentence_obj)
                    sentence_obj[1] = ""
                    sentence_obj[2] = self.list[index].start
                ## if we have the same speaker as the previous instances
                ## just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker

    ## iterates through the list data structure creating the xml file,
    ## which will later be used to generate the chat file
    def print_all_rows_xml(
        self, apply_subelement_root, apply_subelement_word, apply_sentence_end
    ):
        ## initialize setnence speaker to contain first word's speaker
        sentence = apply_subelement_root(self.list[0].speaker)

        ## loop though items in the list data structure
        for index in range(len(self.list)):
            next_utt = self.get_next_utt(self.list[index])
            ## case for if the next speaker doesn't match the current speaker,
            ## meaning there is a change in turns/sentences
            if next_utt == False or next_utt.speaker != self.list[index].speaker:
                ## case for last word in the list
                if index == (len(self.list) - 1):
                    apply_subelement_word(sentence, self.list[index].text)
                    t_elem = apply_sentence_end(sentence)
                    return
                ## case for if there is a word terminating a turn
                if self.is_speaker_utt(self.list[index].speaker):
                    apply_subelement_word(sentence, self.list[index].text)
                    t_elem = apply_sentence_end(sentence)
                    sentence = apply_subelement_root(self.list[index].speaker)
                ## case for if there is a marker (becuase markers will always
                ## have a different speaker)
                else:
                    apply_subelement_word(sentence, self.list[index].speaker)
            ## if we have the same speaker as the previous instances
            ## meaning text is simply added to a sentence
            else:
                apply_subelement_word(sentence, self.list[index].text)
