# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 14:52:57
# @Description: Writes data to disk our list of words and list of sentences

import pickle
import sys
from gailbot.pluginMethod import GBPluginMethods
import threading


class Pickling:
    def __init__(self):
        methods = GBPluginMethods
        self.filepath = methods.temp_work_path
        self.lock = threading.Lock()

    # Save utterance data to disk
    def save_list_to_disk(self, list):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(list, file)

    # Load utterance data from disk
    def load_list_from_disk(self, my_list):
        with self.lock:
            try:
                file = open(str(self.filepath), "rb")
                my_list = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
        return my_list

    # Save utterance data to disk
    def save_sentences_to_disk(self, sentences):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(sentences, file)

    # Load utterance data from disk
    def load_sentences_from_disk(self, sentences):
        with self.lock:
            try:
                with open(str(self.filepath), "rb") as file:
                    sentences = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
            return sentences
