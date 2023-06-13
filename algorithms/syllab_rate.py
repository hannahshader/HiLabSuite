from typing import Dict, Any, List, TypedDict
import syllables
from data_structures.data_objects import UttObj
from data_structures.data_objects import Marker


"""
Takes a single utterance node
Returns a overlap marker to insert
"""


class SYLLAB_DICT(TypedDict):
    utt: List[UttObj]
    syllabNum: int
    syllabRate: float


class SyllableRatePlugin:
    def __init__(self) -> None:
        return None

    def syllab_marker(curr_node):
        """
        Calculates the syllable rates for each utterance and statistics for the
        conversation as a whole, including the median, MAD, fast speech counts and
        slow speech counts
        """

        syllab_sum = 0
        utt_syllb_dict = []

        syllab_num = sum(syllables.estaimte(word.text) for word in curr_node)
        time_diff = abs(curr_node[0].startTime - curr_node[-1].endTime)

        if time_diff == 0:
            print(
                f"get no 0 time difference between words {curr_node[0].text} and {curr_node[-1].text}"
            )
            time_diff = 0.001

        syllab_rate = round(syllab_num / time_diff, 2)
        new_syllab_dict: SYLLAB_DICT = {
            "utt": utt,
            "syllableNum": syllab_num,
            "syllabRate": syllab_rate,
        }

        # TODO insert utterance syllable marker with new_syllab_dict
