from typing import List, Dict


def get_dependencies() -> List[Dict]:
    return [
        {
            "plugin_name": "overlaps",
            "plugin_dependencies": ["conv_model"],
            "plugin_file_path": "analysis/overlaps.py",
            "plugin_source_name": "overlaps",
            "plugin_class_name": "OverlapPlugin",
        },
        {
            "plugin_name": "pauses",
            "plugin_dependencies": ["conv_model"],
            "plugin_file_path": "analysis/pauses.py",
            "plugin_source_name": "pauses",
            "plugin_class_name": "PausePlugin",
        },
        {
            "plugin_name": "gaps",
            "plugin_dependencies": ["conv_model"],
            "plugin_file_path": "analysis/gaps.py",
            "plugin_source_name": "gaps",
            "plugin_class_name": "GapPlugin",
        },
        {
            "plugin_name": "syllable_rate",
            "plugin_dependencies": ["conv_model"],
            "plugin_file_path": "analysis/syllable_rate.py",
            "plugin_source_name": "syllable_rate",
            "plugin_class_name": "SyllableRatePlugin",
        },
    ]
