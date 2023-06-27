# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 14:52:57
# @Description: Writes data to disk our list of words and list of sentences

import pickle
import sys
import threading

from gailbot.pluginMethod import GBPluginMethods


class Pickling:
    # Initializes the methods to save to disk
    def __init__(self):
        methods = GBPluginMethods
        self.filepath = methods.temp_work_path
        self.lock = threading.Lock()

    # Saves the utterance data to disk for the list of words
    def save_list_to_disk(self, list):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(list, file)

    # Loads the disk's utterance data for the list of words
    def load_list_from_disk(self, list):
        with self.lock:
            with open(str(self.filepath), "rb") as file:
                list = pickle.load(file)

    # Saves the utterance data to disk for the list of sentence start/end times
    def save_sentences_to_disk(self, sentences):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(sentences, file)

    # Loads the disk's utterance data for the list of sentence start/end times
    def load_sentences_from_disk(self, sentences):
        with self.lock:
            with open(str(self.filepath), "rb") as file:
                sentences = pickle.load(file)