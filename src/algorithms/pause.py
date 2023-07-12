# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-12 14:37:34
# @Description: Checks for pauses in speech when one speaker is speaking

import logging
import io
from typing import Dict, Any, List
from dataclasses import dataclass

from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    THRESHOLD,
    load_threshold,
)
from Plugin_Development.src.data_structures.data_objects import UttObj

###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################

class PausePlugin:
    """
    Wrapper class for the Pause plugin. Contains functionality that inserts
    overlap markers
    """

    def pause_marker(curr_utt: UttObj, next_utt: UttObj) -> UttObj:
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
        2.  Assert that the nodes are by the same speaker. If they are by
            different speakers, return false
        3.  Subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant gap" between curr_node and
            curr_next_node with given threshold
        4.  If there is a "significant pause," return Pause Marker
        """
        # Pause if uttered by same speaker

        if curr_utt.speaker == next_utt.speaker:

            # Returned to the console
            logging.info("start pause analysis")
            fto = round(next_utt.start - curr_utt.end, 2)
            markerText = ""
            # Check for latch threshold
            if ((load_threshold().LB_LATCH <= fto) 
                and (fto <= load_threshold().UB_LATCH)):
                # Returned to the debug output. Not accessible in GUI
                logging.debug(f"latch detected with fto {fto}")
                # format marker text
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_utt.speaker)
                )
                logging.debug(f"generating latch marker: {markerText}")
                return UttObj(
                    curr_utt.end,
                    next_utt.start,
                    curr_utt.speaker,
                    INTERNAL_MARKER.PAUSES,
                    curr_utt.flexible_info,
                )

            # check for pause threshold
            elif THRESHOLD.LB_PAUSE <= fto <= THRESHOLD.UB_PAUSE:
                logging.debug(f"pause detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 2)), str(curr_utt.speaker)
                )
                logging.debug(f"generating pause marker: {markerText}")
                return UttObj(
                    curr_utt.end,
                    next_utt.start,
                    curr_utt.speaker,
                    INTERNAL_MARKER.PAUSES,
                    curr_utt.flexible_info,
                )
                logging.debug(f"pause marker ({markerText}) generated")
                
            # check for micro pause threshold
            elif THRESHOLD.LB_MICROPAUSE <= fto <= THRESHOLD.UB_MICROPAUSE:
                logging.debug(f"micro pause detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_utt.speaker)
                )
                logging.debug(f"generating micro pause marker: {markerText}")
                return_marker = UttObj(
                    curr_utt.end,
                    next_utt.start,
                    curr_utt.speaker,
                    INTERNAL_MARKER.PAUSES,
                    curr_utt.flexible_info,
                )
                logging.info(f"micro pause marker ({markerText}) generated")
                
            # Check for large pause threshold
            elif fto >= load_threshold().LB_LARGE_PAUSE:
                logging.debug(f"large pause detected with fto {fto}")
                markerText = MARKER.TYPE_INFO_SP.format(
                    MARKER.PAUSES, str(round(fto, 1)), str(curr_utt.speaker)
                )
                logging.debug(f"generating larger pause marker: {markerText}")
                return_marker = UttObj(
                    curr_utt.end,
                    next_utt.start,
                    curr_utt.speaker,
                    INTERNAL_MARKER.PAUSES,
                    curr_utt.flexible_info,
                )
                logging.debug(f"larger pause marker ({markerText}) generated")
        return
