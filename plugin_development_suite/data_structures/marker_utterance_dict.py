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
            sentence_data_plain = []
            speaker = ""
            prev_utt = None
            for key, value in utterance_map.items():
                for utt_dict in value:
                    if utt_dict.speaker != speaker:
                        if prev_utt != None:
                            sentence_data_plain.append(prev_utt.end)
                        sentence_data_plain.append(utt_dict.start)
                        speaker = utt_dict.speaker
                    utt = UttObj(
                        utt_dict.start,
                        utt_dict.end,
                        utt_dict.speaker,
                        utt_dict.text,
                    )
                    utterances.append(utt)
                    prev_utt = utt_dict
                sentence_data_plain.append((value[-1]).end)

            sentence_data = []
            for i in range(0, len(sentence_data_plain), 2):
                sublist = [sentence_data_plain[i], sentence_data_plain[i + 1]]
                sentence_data.append(sublist)

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

        sentences_copy = copy.deepcopy(self.sentences)
        list_copy = copy.deepcopy(self.list)

        utt_list = []
        sentence_index = 0
        while sentence_index < len(sentences_copy):
            utt_index = 0
            while utt_index < len(list_copy):
                sentence = sentences_copy[sentence_index]
                utt = list_copy[utt_index]
                if sentence[0] <= utt.start <= sentence[1]:
                    if self.is_speaker_utt(utt.speaker) != False:
                        utt_list.append(utt)
                    utt_index += 1
                else:
                    func(utt_list, sentence[0], sentence[1])
                    utt_list = []
                    sentence_index += 1

            sentence_index += 1

        self.pickle.save_sentences_to_disk(self.sentences)
        self.pickle.save_list_to_disk(self.list)

        """
        for curr_sentence in self.sentences:
            ## using second list item, get the sentence end time
        sentence_end_time = curr_sentence[1]
        for curr_item in self.list:
            print("current item is")
            print(curr_item)
            if curr_item.start > sentence_end_time:
                break
            if self.is_speaker_utt(curr_item.speaker) == False:
                continue
            else:
                func(curr_item, curr_sentence[0], curr_sentence[1])
                self.pickle.save_sentences_to_disk(self.sentences)
                self.pickle.save_list_to_disk(self.list)
        """

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

    def print_all_rows_text(self, format_markers, outfile, formatter):
        ##speaker, text, start, end
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            ## if not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                ##sentence_obj[1] += self.list[index].speaker + " "
                sentence_obj[1] += format_markers(self.list[index])
            else:
                ## gets the next utterance. gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                ## if the next index is from a different speaker
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
                    outfile.write(write_string)
                    sentence_obj[1] = ""
                    sentence_obj[2] = self.list[index].start
                ## if we have the same speaker as the previous instances
                ## just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker

    ## creates the csv output for Gailbot, separating each line by its speaker
    def print_all_rows_csv(self, print_func, format_markers):
        ##speaker, text, start, end
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            ## if not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                ##sentence_obj[1] += self.list[index].speaker + " "
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

    def print_all_rows_chat(self, format_markers):
        ##speaker, text, start, end
        string_result = ""
        sentence_obj = ["", "", 0, 0]
        for index in range(len(self.list)):
            ## if not a speaker, then add text and continue
            if self.is_speaker_utt(self.list[index].speaker) == False:
                ##sentence_obj[1] += self.list[index].speaker + " "
                sentence_obj[1] += format_markers(self.list[index])
            else:
                ## gets the next utterance. gives false if end of list
                next_utt = self.get_next_utt(self.list[index])
                ## if the next index is from a different speaker
                if next_utt == False or next_utt.speaker != self.list[index].speaker:
                    sentence_obj[3] = self.list[index].end
                    sentence_obj[1] += self.list[index].text
                    sentence_obj[0] = self.list[index].speaker
                    ## makes sure that the string doesn't have any trailing white space
                    string_result += (
                        "*" + sentence_obj[0] + ":\t" + sentence_obj[1].rstrip() + "\n"
                    )
                    sentence_obj[1] = ""
                    sentence_obj[2] = self.list[index].start
                ## if we have the same speaker as the previous instances
                ## just add the text to the end of the line
                else:
                    sentence_obj[1] += self.list[index].text + " "
                    if self.is_speaker_utt(self.list[index].speaker):
                        sentence_obj[0] = self.list[index].speaker
        print("string result is")
        print(string_result)
        return string_result
