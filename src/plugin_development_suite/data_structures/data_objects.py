# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 15:34:43
# @Description: All necessary data objects for the dictionaries

from dataclasses import dataclass
import os

@dataclass
class UttObj:
    """
    Format:
    -------
        Start time for utterance,

        End time for utterance,
        
        The speaker of the utterance,
        
        The utterance itself
    """
    start: float
    end: float
    speaker: str
    text: str