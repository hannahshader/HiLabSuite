from typing import Dict, Any, List, Tuple
import re
import io
import os

# Local imports
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


class OutputFileManager:
    def __init__(self):
        # populate data structure with plugins
        structure_interact_instance = StructureInteract()
        methods = GBPluginMethods()
        structure_interact_instance = structure_interact_instance.apply(methods)

        ## create the CSV files
        csv_init = CSVPlugin()
        csv_init.apply(structure_interact_instance)

        text_init = TextPlugin()
        text_init.apply(structure_interact_instance)
