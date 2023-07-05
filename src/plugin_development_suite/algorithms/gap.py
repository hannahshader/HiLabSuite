# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-27 12:16:07
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-06-29 10:55:44
from typing import Dict, Any, List
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


###############################################################################
# GLOBALS                                                                     #
###############################################################################
MARKER = INTERNAL_MARKER  # gets class representing a marker node
THRESHOLD = load_threshold()  # function to retrieve threshold data from config


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################
class GapPlugin:
    """
    Wrapper class for the Gaps plugin. Contains functionality that inserts
    gap markers
    """

    def gap_marker(curr_utt: UttObj, next_utt: UttObj) -> UttObj:
        """
        Parameters
        ----------
        curr_utt : UttObj
            Utterance object representing the current utterance
        next_utt: UttObj
            Utterance object representing the next utterance

        Returns
        -------
        An utterance object representing a marker node

        Algorithm:
        ----------
        1.  Takes in curr_node and get curr_next_node
        2.  Assert that the nodes are by different speakers. If they are by
        the same speakers, return false
        3.  Subtract start time of curr_next_node from end time of curr_node.
        Assert that there is "significant gap" between curr_node and
        curr_next_node with given threshold
        4.  If there is "significant gap," create and return a Gap Marker
        """
        fto = round(next_utt.start - curr_utt.end, 2)
        logging.debug(f"get fto : {fto}")
        if fto >= THRESHOLD.GAPS_LB and curr_utt.speaker != next_utt.speaker:
            logging.debug(f"get fto : {fto}")
            # Format marker text
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr_utt.speaker)
            )
            # Creates a marker instance
            return UttObj(
                start=curr_utt.end,
                end=next_utt.start,
                speaker=MARKER.GAPS,
                text=markerText,
            )