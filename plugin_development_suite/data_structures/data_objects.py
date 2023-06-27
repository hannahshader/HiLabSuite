# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 15:04:14
# @Description: All necessary data objects for the dictionaries

import os
from dataclasses import dataclass

@dataclass
# Format:
# Start time for utterance,
# End time for utterance, 
# The speaker of the utterance
# The utterance itself
class UttObj:
    start: float
    end: float
    speaker: str
    text: str
