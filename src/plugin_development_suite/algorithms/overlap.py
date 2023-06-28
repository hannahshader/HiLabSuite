# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 14:41:55
# @Description: Checks for overlaps between multiple speakers

from typing import Dict, Any, List

from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

############
# GLOBALS
############

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()
INVALID_OVERLAP = (-1, -1, -1, -1)

############
# CLASS DEFINITIONS
############


class OverlapPlugin:
    def overlap_marker(curr_sentence, next_sentence) -> List[str]:
        """
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
