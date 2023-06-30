# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-06-30 17:02:54
# @Description: Checks for overlaps between multiple speakers

from typing import Dict, Any, List

from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj


MARKER = INTERNAL_MARKER
""" The format of the marker to be inserted into the list """
THRESHOLD = load_threshold()
""" The threshold for what length of time qualifies an 'overlap' """
INVALID_OVERLAP = (-1, -1, -1, -1)
""" A dummy format for an invalid overlap """

###############################################################################
# GLOBALS                                                                     #
###############################################################################

MARKER = INTERNAL_MARKER  # gets class representing a marker node
THRESHOLD = load_threshold()  # function to retrieve threshold data from config
INVALID_OVERLAP = (-1, -1, -1, -1)  # markers for an invalid overlap


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################


class OverlapPlugin:
    """
    Wrapper class for the Overlap plugin. Contains functionality that inserts
    overlap markers
    """

    def overlap_marker(
        curr_sentence: List[List], next_sentence: List[List]
    ) -> List[str]:
        """
        Parameters
        ----------
        curr_sentence : List[List[float]]
            List of sentences represented in a list by start and end times
        next_sentence: List[List[float]]
            List of sentences represented in a list by start and end times

        Returns
        -------
        Four overlap markers. Overlap start and end markers for each speaker

        Algorithm: modified
        1. Given current sentence and next sentence
        2. Check if: next.start < curr.end
        3. If no, not an overlap
        4. If yes:
            curr overlap start marker = next.start
                curr overlap end marker = min(curr.end, next.end)
        5. Return two markers

        """
        # Define markers
        curr_start, curr_end = curr_sentence[0], curr_sentence[1]
        next_start, next_end = next_sentence[0], next_sentence[1]

        # Overlap exist when next_start < curr_end
        if next_start < curr_end:
            # Set overlap start marker
            overlap_start_time = next_start
            overlap_start = UttObj(
                overlap_start_time,
                overlap_start_time,
                MARKER.OVERLAPS,
                "overlap_start",
            )
            # Set overlap end marker
            overlap_end_time = min(curr_end, next_end)
            overlap_end = UttObj(
                overlap_end_time,
                overlap_end_time,
                MARKER.OVERLAPS,
                "overlap_end",
            )
            return [overlap_start, overlap_end]
        else:
            return []
