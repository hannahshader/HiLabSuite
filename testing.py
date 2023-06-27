# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 15:09:28
# @Description: Tests creation of the instance of file output

import os
import csv
from typing import Dict, Any
from pydantic import BaseModel
from dataclasses import dataclass

from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.format.csv import CSVPlugin
from plugin_development_suite.format.chat import ChatPlugin
from plugin_development_suite.format.output_file_manager import (
    OutputFileManager
)
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)

# Initializes the object that runs the program
output_file_manager_init = OutputFileManager()
