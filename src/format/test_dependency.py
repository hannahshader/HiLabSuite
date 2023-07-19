# -*- coding: utf-8 -*-
# @Author: Hannah Shader
# @Date:   2023-07-12 12:16:59
# @Last Modified by:   Hannah Shader
# @Last Modified time: 2023-07-12 15:35:53

"""
import re
import io
import os
import shutil
from typing import Dict, Any, List, Tuple

from gailbot import Plugin
from gailbot import GBPluginMethods
from HiLabSuite.src.data_structures.structure_interact import (
    StructureInteract,
)
from HiLabSuite.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    OUTPUT_FILE,
    CON_FORMATTER,
)
from HiLabSuite.src.format.csv import CSVPlugin
from HiLabSuite.src.format.text import TextPlugin
from HiLabSuite.src.format.xml import XmlPlugin
from HiLabSuite.src.format.chat import ChatPlugin


class TestDependency(Plugin):
    def __init__(self):
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        structure_interact_instance = dependency_outputs["OutputFileManager"]
        structure_interact_instance.testing_print()

        self.successful = True
        return True
"""
