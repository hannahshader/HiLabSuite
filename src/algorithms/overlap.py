# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-12 14:36:46
# @Description: Checks for overlaps between multiple speakers

from typing import Dict, Any, List
import logging

from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
)
from Plugin_Development.src.data_structures.data_objects import UttObj

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################

class OverlapPlugin:
    """
    Wrapper class for the Overlap plugin. Contains functionality that inserts
    overlap markers
    """

    def OverlapMarker(curr_sentence, next_sentence, list) -> List[str]:
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

        # define markers
        curr_start, curr_end, curr_id = (
            curr_sentence[0],
            curr_sentence[1],
            curr_sentence[2],
        )
        next_start, next_end, next_id = (
            next_sentence[0],
            next_sentence[1],
            next_sentence[2],
        )

        # overlap exist when next_start < curr_end
        if next_start < curr_end:
            curr_speaker = ""
            next_speaker = ""
            for utt in list:
                if utt.start == next_start and utt.flexible_info == next_id:
                    next_speaker = utt.speaker
                    next_flexible_info = utt.flexible_info

                if utt.end == curr_end and utt.flexible_info == curr_id:
                    curr_speaker = utt.speaker
                    curr_flexible_info = utt.flexible_info

            # set overlap start marker
            overlap_start_time = max(curr_start, next_start)
            overlap_start_one = UttObj(
                overlap_start_time,
                overlap_start_time,
                curr_speaker,
                INTERNAL_MARKER.OVERLAP_FIRST_START,
                curr_flexible_info,
            )
            overlap_start_two = UttObj(
                overlap_start_time,
                overlap_start_time,
                next_speaker,
                INTERNAL_MARKER.OVERLAP_SECOND_START,
                next_flexible_info,
            )
            # set overlap end marker
            overlap_end_time = min(curr_end, next_end)
            overlap_end_one = UttObj(
                overlap_end_time,
                overlap_end_time,
                curr_speaker,
                INTERNAL_MARKER.OVERLAP_FIRST_END,
                curr_flexible_info,
            )
            overlap_end_two = UttObj(
                overlap_end_time,
                overlap_end_time,
                next_speaker,
                INTERNAL_MARKER.OVERLAP_SECOND_END,
                next_flexible_info,
            )

            return [
                overlap_start_two,
                overlap_start_one,
                overlap_end_one,
                overlap_end_two,
                curr_flexible_info,
                next_flexible_info,
            ]
        else:
            return []
