# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-06-27 12:16:07
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-27 13:00:28


from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.data_structures.data_objects import UttObj
from plugin_development_suite.format.csv import CSVPlugin
from plugin_development_suite.format.chat import ChatPlugin
from plugin_development_suite.format.output_file_manager import (
    OutputFileManager,
)
from typing import Dict, Any
from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
import os
import csv
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)


##from data_structures.data_objects import UttObj
from pydantic import BaseModel
from dataclasses import dataclass

output_file_manager_init = OutputFileManager()
