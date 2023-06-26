from typing import Dict, Any, List
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()
INVALID_OVERLAP = (-1, -1, -1, -1)

"""
Take utterance pair and return a overlap markers to insert
"""


class OverlapPlugin:
    def OverlapMarker(curr_sentence, next_sentence):
        """
        Algorithm: modified
        1. given current sentence and next sentence
        2. check if: next.start < curr.end
        3. if no, not an overlap
        4. if yes:
            curr overlap start marker = next.start
            curr overlap end marker = min(curr.end, next.end)
        5. return two markers

        """
        curr_start, curr_end = curr_sentence[0], curr_sentence[1]
        next_start, next_end = next_sentence[0], next_sentence[1]

        if next_start < curr_end:
            overlap_start_time = next_start
            overlap_start = UttObj(
                overlap_start_time,
                overlap_start_time,
                MARKER.OVERLAPS,
                "overlap_start",
            )

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
