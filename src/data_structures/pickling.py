# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Hannah Shader
# @Last Modified time: 2023-07-06 11:03:29
# @Description: Writes data to disk our list of words and list of sentences

import pickle
import sys
import os
from gailbot import GBPluginMethods
import threading


class Pickling:
    def __init__(self):
        """
        methods = GBPluginMethods
        self.filepath = methods.temp_work_path
        self.lock = threading.Lock()
        pass
        """

    def save_list_to_disk(self, list: list[any]) -> None:
        """
        Save utterance data to disk

        Parameters
        ----------
        list: the list to save to the disk

        Returns
        -------
        None
        """
        """
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(list, file)
        """

    def load_list_from_disk(self, my_list: list[any]) -> list[any]:
        """
        Load utterance data from disk

        Parameters
        ----------
        my_list: the list to return from the disk

        Returns
        -------
        a list that has been returned
        """
        """
        with self.lock:
            try:
                with open(str(self.filepath), "rb") as file:
                    # new file length checking version
                    file_info = os.fstat(file.fileno())
                    file_size = file_info.st_size
                    if file_size > 0:  # Check if the file is not empty
                        my_list = pickle.load(file)

                    # commented out: original version
                    # my_list = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
        return my_list
        """

    def save_sentences_to_disk(self, sentences: list[str]) -> None:
        """
        Save utterance data to disk

        Parameters
        ----------
        sentences: the sentences to save to the disk

        Returns
        -------
        none
        """
        """
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(sentences, file)
        """

    def load_sentences_from_disk(self, sentences: list[str]) -> list[str]:
        """
        Load utterance data from disk

        Parameters
        ----------
        sentences: the list to return from the disk

        Returns
        -------
        a list that has been returned
        """
        """
        with self.lock:
            try:
                with open(str(self.filepath), "rb") as file:
                    # new file length checking version
                    file_info = os.fstat(file.fileno())
                    file_size = file_info.st_size
                    if file_size > 0:  # Check if the file is not empty
                        sentences = pickle.load(file)
                    
                    # commented out: original version
                    # sentences = pickle.load(file)
            ## case for if file already open
            except IOError:
                pass
        
        return sentences
        """
