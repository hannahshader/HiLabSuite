# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:43:41
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

    def save_list_to_disk(self, list):
        """
        Save utterance data to disk
        """
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(list, file)

    def load_list_from_disk(self, my_list):
        """
        Load utterance data from disk
        """
        with self.lock:
            try:
                file = open(str(self.filepath), "rb")
                my_list = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
        return my_list

    def save_sentences_to_disk(self, sentences):
        """
        Save utterance data to disk
        """
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(sentences, file)

    def load_sentences_from_disk(self, sentences):
        """
        Load utterance data from disk
        """
        with self.lock:
            try:
                with open(str(self.filepath), "rb") as file:
                    sentences = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
            return sentences
