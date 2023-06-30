# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-06-28 16:36:23
# @Description: Replicates the input from the Gailbot app for testing purposes

import os
from typing import Dict, Union, List, Any
from pydantic import BaseModel
from gailbot import Methods


class UttObj(BaseModel):
    start: float
    end: float
    speaker: str
    text: str


class GBPluginMethods(Methods):
    """ """

    def get_utterance_objects(self) -> Dict[str, List[UttObj]]:
        return {
            "test recording": [
                UttObj(start=0.51, end=0.77, speaker="0", text="okay"),
                UttObj(start=0.77, end=0.93, speaker="0", text="I've"),
                UttObj(start=0.93, end=1.22, speaker="0", text="started"),
                UttObj(start=1.22, end=1.77, speaker="0", text="talking"),
                UttObj(start=2.07, end=2.62, speaker="0", text="%HESITATION"),
                UttObj(start=2.85, end=3.12, speaker="0", text="yeah"),
                UttObj(start=3.12, end=3.18, speaker="0", text="I"),
                UttObj(start=3.18, end=3.47, speaker="0", text="was"),
                UttObj(start=3.47, end=3.73, speaker="0", text="talking"),
                UttObj(start=3.73, end=3.82, speaker="0", text="to"),
                UttObj(start=3.82, end=4.23, speaker="0", text="sametime"),
                UttObj(start=4.23, end=4.48, speaker="0", text="someone"),
                UttObj(start=4.48, end=4.7, speaker="0", text="talk"),
                UttObj(start=5.6, end=5.87, speaker="0", text="yeah"),
                UttObj(start=6.26, end=6.55, speaker="0", text="all"),
                UttObj(start=6.55, end=6.81, speaker="0", text="talk"),
                UttObj(start=6.81, end=6.89, speaker="0", text="at"),
                UttObj(start=6.89, end=7.0, speaker="0", text="the"),
                UttObj(start=7.0, end=7.34, speaker="0", text="same"),
                UttObj(start=7.34, end=7.72, speaker="0", text="time"),
                UttObj(start=7.72, end=7.83, speaker="0", text="we're"),
                UttObj(start=7.83, end=8.05, speaker="0", text="all"),
                UttObj(start=8.05, end=8.31, speaker="0", text="talking"),
                UttObj(start=9.12, end=9.38, speaker="1", text="please"),
                UttObj(start=9.38, end=9.59, speaker="1", text="take"),
                UttObj(start=9.59, end=9.73, speaker="1", text="my"),
                UttObj(start=9.73, end=9.97, speaker="1", text="best"),
                UttObj(start=9.97, end=10.09, speaker="1", text="buy"),
                UttObj(start=10.09, end=10.18, speaker="1", text="the"),
                UttObj(start=10.18, end=10.44, speaker="1", text="different"),
                UttObj(start=10.44, end=10.97, speaker="1", text="speakers"),
                UttObj(start=11.73, end=12.14, speaker="0", text="and"),
                UttObj(start=12.17, end=12.4, speaker="0", text="now"),
                UttObj(start=12.4, end=12.69, speaker="0", text="let's"),
                UttObj(start=12.69, end=12.88, speaker="0", text="do"),
                UttObj(start=12.88, end=13.42, speaker="0", text="some"),
                UttObj(start=13.42, end=13.64, speaker="0", text="where"),
                UttObj(start=13.64, end=13.86, speaker="0", text="we're"),
                UttObj(start=13.86, end=14.25, speaker="0", text="just"),
                UttObj(start=14.25, end=14.68, speaker="0", text="talking"),
                UttObj(start=14.68, end=14.85, speaker="0", text="some"),
                UttObj(start=14.85, end=14.98, speaker="0", text="of"),
                UttObj(start=14.98, end=15.32, speaker="0", text="us"),
                UttObj(start=18.1, end=18.55, speaker="1", text="sure"),
                UttObj(start=22.01, end=22.4, speaker="1", text="yeah"),
                UttObj(start=22.43, end=23.12, speaker="1", text="%HESITATION"),
                UttObj(start=23.31, end=23.84, speaker="1", text="%HESITATION"),
                UttObj(start=23.92, end=24.13, speaker="1", text="let's"),
                UttObj(start=24.13, end=24.26, speaker="1", text="see"),
                UttObj(start=24.26, end=24.37, speaker="1", text="if"),
                UttObj(start=24.37, end=24.57, speaker="1", text="this"),
                UttObj(start=24.57, end=25.12, speaker="1", text="works"),
                UttObj(start=26.85, end=27.22, speaker="0", text="%HESITATION"),
                UttObj(start=28.17, end=28.66, speaker="0", text="hi"),
                UttObj(start=28.66, end=28.99, speaker="0", text="Lester"),
            ],
            "test recording 2": [
                UttObj(start=23.92, end=24.13, speaker="0", text="hey"),
                UttObj(start=24.17, end=25.05, speaker="0", text="there"),
                UttObj(start=25.10, end=25.25, speaker="0", text="man"),
            ],
        }

    @property
    def output_path(self) -> str:
        return "/Users/jasonycwu/Documents/GitHub/Plugin-Development/Plugin-Development-Output"
        return "/Users/hannahshader/Desktop/Plugin-Development-Output"

    @property
    def temp_work_path(self) -> str:
        """
        Accesses and returns the temporary workspace path
        Returns:
            String containing the temporary workspace path
        """
        return "/Users/jasonycwu/Documents/GitHub/Plugin-Development/Temp_Workspace"
        return "/Users/hannahshader/Desktop/Temp_Workspace"

    # jar path
    @property
    def chatter_path(self) -> str:
        return
        return "/Users/hannahshader/Desktop/chatter/chatter.jar"
