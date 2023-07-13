# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-07-13 11:47:50
# @Description: Manages the output files created by our plugins

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


class OutputFileManager(Plugin):
    """
    Creates file objects and runs drivers
    """

    def __init__(self):
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Populate the data structure with plugins
        """
        # populate data structure with plugins
        structure_interact_instance = StructureInteract()
        structure_interact_instance = structure_interact_instance.apply(methods)

        self.successful = True
        return structure_interact_instance

        ## creates all files
        """
        csv_init = CSVPlugin()
        csv_init.run(structure_interact_instance)

        text_init = TextPlugin()
        text_init.run(structure_interact_instance)

        xml_init = XmlPlugin()
        xml_init.run(structure_interact_instance)

        chat_init = ChatPlugin()
        chat_init.run(structure_interact_instance)

        audio_file_path = methods.output_path.replace(
            "/Analysis/Plugin_Development", "/Raw/Media/merged.wav"
        )
        shutil.copy2(audio_file_path, methods.output_path)

        self.successful = True
        """
