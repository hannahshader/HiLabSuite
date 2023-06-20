import pickle
import sys
from gailbot.pluginMethod import GBPluginMethods
import threading


class Pickling:
    """
    load_items = 100
    """

    def __init__(self):
        """
        self.load_items = 100
        self.list_item_size = sys.getsizeof(data_strucutre_instance.list[0])
        self.sentence_item_size = sys.getsizeof(data_strucutre_instance.sentences[0])
        """
        methods = GBPluginMethods
        self.filepath = methods.temp_work_path
        self.lock = threading.Lock()

    # Save utterance data to disk
    def save_list_to_disk(self, list):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(list, file)

    # Load utterance data from disk
    def load_list_from_disk(self, list):
        with self.lock:
            with open(str(self.filepath), "rb") as file:
                list = pickle.load(file)

    # Save utterance data to disk
    def save_sentences_to_disk(self, sentences):
        with self.lock:
            with open(str(self.filepath), "wb") as file:
                pickle.dump(sentences, file)

    # Load utterance data from disk
    def load_sentences_from_disk(self, sentences):
        with self.lock:
            with open(str(self.filepath), "rb") as file:
                sentences = pickle.load(file)


"""
    def pickle_for_loop(self, func):
        with open(self.filepath, "rb+") as file:

            # Read and unpickle sections of the file until the end is reached
            while True:
                try:
                    # Read the next section from the file
                    section = []
                    for _ in range(self.load_items):
                        item = pickle.load(file)
                        section.append(item)

                    # Process the section
                    processed_section = []
                    prev_item = None
                    for item in section:
                        for func in apply_functions:
                            marker = func(curr, curr_next)
                            self.insert_marker(marker)
                        # Perform operations on the item
                        processed_section.append(item)

                    # Repickle the processed section back to the file
                    file.seek(file.tell() - (self.load_items * self.list_item_size))
                    for processed_item in processed_section:
                        pickle.dump(processed_item, file)

                except EOFError:
                    break
                    
    def pickle_for_loop_helper(item_prev, item, apply_functions):
        for func in apply_functions:
                marker = func(curr, curr_next)
                self.insert_marker(marker)

        
"""
