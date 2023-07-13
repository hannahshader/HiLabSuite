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
from Plugin_Development.src.data_structures.structure_interact import (
    StructureInteract,
)
from Plugin_Development.src.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CON_FORMATTER,
)
from Plugin_Development.src.format.csv import CSVPlugin
from Plugin_Development.src.format.text import TextPlugin
from Plugin_Development.src.format.xml import XmlPlugin
from Plugin_Development.src.format.chat import ChatPlugin


class TestDependency(Plugin):
    def __init__(self):
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        structure_interact_instance = dependency_outputs["OutputFileManager"]
        structure_interact_instance.testing_print()

        self.successful = True
        return True
"""
