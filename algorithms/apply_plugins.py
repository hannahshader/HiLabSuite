from algorithms.init import get_dependencies
from algorithms.gap import GapPlugin as gap
from algorithms.overlap import OverlapPlugin as overlap
from algorithms.pause import PausePlugin as pause
from algorithms.syllab_rate import SyllableRatePlugin as syllab_rate
from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, TypeVar
import toml


class ApplyPlugins:
    def __init__(self, config_file_path):
        self.plugins = self.function_list(config_file_path)

    def function_names(self, file_path):
        with open(file_path, "r") as file:
            config_data = toml.load(file)
        plugin_names = []
        if "plugins" in config_data:
            for plugin in config_data["plugins"]:
                if "plugin_name" in plugin:
                    plugin_names.append(plugin["plugin_name"])
        return plugin_names

    def function_list(self, config_file_path):
        plugin_names = self.function_names(config_file_path)
        if "overlaps" in plugin_names:
            result += overlap.add_overlap_marker
        if "pauses" in plugin_names:
            result += pause.add_pause_marker
        if "gaps" in plugin_names:
            result += gap.add_gap_marker
        if "syllable_rate" in plugin_names:
            result += syllab_rate.add_syllab_marker
        return result

    def apply_plugins(self, structure_interact_instance):
        self.structure_interact_instance.apply_markers(
            structure_interact_instance, self.plugins
        )
