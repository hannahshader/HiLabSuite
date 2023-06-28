# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-28 13:53:35
# @Description: Manages the output files created by our plugins

import re
import io
import os
from typing import Dict, Any, List, Tuple

from gailbot.plugin import Plugin
from gailbot.pluginMethod import GBPluginMethods
from plugin_development_suite.data_structures.structure_interact import (
    StructureInteract,
)
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CON_FORMATTER,
)
from plugin_development_suite.format.csv import CSVPlugin
from plugin_development_suite.format.text import TextPlugin
from plugin_development_suite.format.xml import XmlPlugin
from plugin_development_suite.format.chat import ChatPlugin


class OutputFileManager:
    # Creates file objects and runs drivers
    def __init__(self):
        # Populate the data structure with plugins
        structure_interact_instance = StructureInteract()
        methods = GBPluginMethods()
        structure_interact_instance = structure_interact_instance.apply(methods)

        # Creates the CSV, text, and CHAT files
        csv_init = CSVPlugin()
        csv_init.run(structure_interact_instance)

        text_init = TextPlugin()
        text_init.run(structure_interact_instance)

        xml_init = XmlPlugin()
        xml_init.run(structure_interact_instance)
