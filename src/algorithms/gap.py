# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-27 12:16:07
# @Last Modified by:   Hannah Shader
<<<<<<< Updated upstream
# @Last Modified time: 2023-07-07 15:09:43
=======
# @Last Modified time: 2023-07-13 11:07:31
>>>>>>> Stashed changes
from typing import Dict, Any, List
from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    THRESHOLD,
    load_threshold,
)
from Plugin_Development.src.data_structures.data_objects import UttObj

import logging
<<<<<<< Updated upstream
=======
from gailbot import Plugin
from gailbot import GBPluginMethods
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
class GapPlugin:
=======
class GapPlugin(Plugin):
>>>>>>> Stashed changes
    """
    Wrapper class for the Gaps plugin. Contains functionality that inserts
    gap markers
    """

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        self.structure_interact_instance = dependency_outputs["SyllableRatePlugin"]

        # TODO fix apply marker so you don't need to pass through a list
        functions_list = [GapPlugin.gap_marker]
        self.structure_interact_instance.apply_markers(functions_list)

        self.successful = True
        return self.structure_interact_instance

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
            # format marker text
            markerText = MARKER.TYPE_INFO_SP.format(
                MARKER.GAPS, str(round(fto, 1)), str(curr_utt.speaker)
            )
            # create instance of marker
            return UttObj(
                start=curr_utt.end,
                end=next_utt.start,
                speaker=curr_utt.speaker,
                text=INTERNAL_MARKER.GAPS,
                flexible_info=curr_utt.flexible_info,
            )
