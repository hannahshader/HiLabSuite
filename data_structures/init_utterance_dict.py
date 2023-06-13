from dataclasses import dataclass
import logging
from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel
import os
from collections import OrderedDict
from data_structures.data_objects import UttObj


class InitUtteranceDict:
    def __init__(self, utt_data=None, output_path=None):
        ##self.data stores the raw uttance data
        data = dict()
        if utt_data:
            self.data = utt_data
        else:
            self.data = data

        ##utterance_map stores the sorted utterance_data
        self.utterance_map: Dict[
            str, List[UttObj]
        ] = self.get_utterance_objects_sorted()

    def get_utterance_objects_sorted(self) -> Dict[str, List[UttObj]]:
        """
        Access and return the utterance data as utterance object
        """

        res = dict()
        for key, uttlist in self.data.items():
            newlist = list()
            for utt in uttlist:
                newlist.append(UttObj(**utt))
            res[key] = newlist

        for key in res:
            res[key] = sorted(res[key], key=lambda x: x.start)
        result = OrderedDict(res)
        return result
