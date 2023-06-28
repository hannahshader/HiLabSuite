# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-27 12:16:07
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 13:47:09
from typing import Dict, Any, List

# TODO: Change all imports to this method.
from plugin_development_suite.configs import (
    INTERNAL_MARKER,
    THRESHOLD,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj

import logging

# For logging to STDOUT. Additional handlers can be added for log file outputs.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# TODO: Change logging in all files to this system.


# TODO: GLobal vars. / constants should have a description.
MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()
"""
Take two word nodes next to each other
Return a gap marker to insert
"""


class GapPlugin:
    def gap_marker(curr_utt, next_utt):
        """
        Algorithm:
        1.  Takes in curr_node and get curr_next_node
        2.  Assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  Subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and 
            curr_next_node with given threshold
        4.  If there is "significant gap," create and return a Gap Marker
        """
        fto = round(next_utt.start - curr_utt.end, 2)
        logging.debug(f"get fto : {fto}")
        if fto >= THRESHOLD.GAPS_LB and curr_utt.speaker != next_utt.speaker:
            logging.debug(f"get fto : {fto}")
            # format marker text
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr_utt.speaker)
            )
            # Creates a marker instance
            return UttObj(
                start = curr_utt.end,
                end = next_utt.start,
                speaker = MARKER.GAPS,
                text = markerText,
            )
