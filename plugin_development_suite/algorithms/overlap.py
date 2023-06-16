from typing import Dict, Any, List
from plugin_development_suite.data_structures.data_objects import (
    INTERNAL_MARKER,
    load_threshold,
)
from plugin_development_suite.data_structures.data_objects import UttObj
​
MARKER = INTERNAL_MARKER
THRESHOLD = load_threshold()
INVALID_OVERLAP = (-1, -1, -1, -1)
​
"""
Take utterance pair and return a overlap markers to insert
"""
​
​
class OverlapPlugin:
    def OverlapMarker(curr_utt, next_utt):
        """
        Algorithm:
        1.  takes in curr_node and get curr_next_node
        2.  assert that the nodes are by different speakers. If they are by
            the same speakers, return false
        3.  subtract start time of curr_next_node from end time of curr_node
            assert that there is "significant overlap" between curr_node and curr_next_node
            with given threshold
        4.  if there is "significant overlap," return Overlap Marker
        """
​
        # In the case of an overlap, get its 4 marker positions
        overlap_plugin_instance = OverlapPlugin()
        unique_id = 0
​
        if next_utt.start < curr_utt.end:
            curr_x, curr_y, next_x, next_y = overlap_plugin_instance._get_overlap_positions(curr_utt, next_utt)
            if (curr_x, curr_y, next_x, next_y) == INVALID_OVERLAP:
                print("INVALID: overlap between same speaker detected")
            else:
                if curr_x >= len(curr_utt.text):
                    curr_x = -1
                if next_x >= len(next_utt.text):
                    next_x = -1
                if curr_y >= len(curr_utt.text):
                    curr_y = -1
                if next_y >= len(next_utt.text):
                    next_y = -1
​
                fst_start = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_START, str(unique_id), curr_utt.speaker
                )
                fst_end = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_END, str(unique_id), curr_utt.speaker
                )
                snd_start = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_START, str(unique_id), next_utt.speaker
                )
                snd_end = MARKER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_END, str(unique_id), next_utt.speaker
                )
​
                # insert the overlap markers into the tree
                return_marker_1 = UttObj(
                    curr_utt.start,
                    curr_utt.start,
                    MARKER.OVERLAPS,
                    fst_start,
                )
                return_marker_2 = UttObj(
                    curr_utt.end,
                    curr_utt.end,
                    MARKER.OVERLAPS,
                    fst_end,
                )
                return_marker_3 = UttObj(
                    next_utt.start,
                    next_utt.start,
                    MARKER.OVERLAPS,
                    snd_start,
                )
                return_marker_4 = UttObj(
                    next_utt.end,
                    next_utt.end,
                    MARKER.OVERLAPS,
                    snd_end,
                )
                unique_id += 1
​
                overlap_markers_list = [
                    return_marker_1,
                    return_marker_2,
                    return_marker_3,
                    return_marker_4,
                ]
​
                ##return overlap_markers_list
                return overlap_markers_list
        else:
            return []
​
    def _get_overlap_positions(self, curr_utt, next_utt):
        """
        Return the position of where the overlap markers should be inserted.
        """
​
        # check speaker label
        if curr_utt.speaker == next_utt.speaker:
            return INVALID_OVERLAP
​
        # when there is an overlap and diff speakers
        next_start = next_utt.start
        next_end = next_utt.end
        curr_start = curr_utt.start
        curr_end = curr_utt.end
​
        # do dummy value
        curr_overlap_start_pos = 0
        curr_overlap_end_pos = 0
​
        # current utterance
        if curr_start < next_end and curr_end > next_start:
            if curr_overlap_start_pos != 0 and curr_overlap_end_pos == 0:
                curr_overlap_end_pos = curr_overlap_start_pos
                curr_overlap_end_pos += 1
            else:
                curr_overlap_end_pos += 1
        else:
            if curr_overlap_end_pos == 0:
                curr_overlap_start_pos += 1
​
        next_overlap_start_pos = 0
        next_overlap_end_pos = len(next_utt.text) - 1
​
        # next utterance
        if next_start < curr_end and next_end > curr_start:
            if next_overlap_start_pos != 0 and next_overlap_end_pos == 0:
                next_overlap_end_pos = next_overlap_start_pos
                next_overlap_end_pos += 1
            else:
                next_overlap_end_pos += 1
        else:
            if next_overlap_end_pos == 0:
                next_overlap_start_pos += 1
        
        # check for invalid overlap
        if curr_overlap_end_pos == 0 and next_overlap_end_pos == 0:
            return INVALID_OVERLAP
​
        return (
            curr_overlap_start_pos,
            curr_overlap_end_pos,
            next_overlap_start_pos,
            next_overlap_end_pos,
        )