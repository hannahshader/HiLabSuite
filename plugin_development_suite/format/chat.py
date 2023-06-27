# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-26 12:15:56
# @Last Modified by:   Jacob Boyar
# @Last Modified time: 2023-06-26 15:37:00
# @Description: Creates the CHAT output for our plugins based on TalkBank format

import subprocess
from typing import Dict, Any
import os
import io
from plugin_development_suite.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CSV_FORMATTER,
)


class ChatPlugin:
    ## generates Chat file from Xml file
    def run(self, structure_interact_instance):
        ## gets filepaths
        input_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

        output_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT
        )

        jar_path = structure_interact_instance.chatter_path

        ## runs commands
        command = f"java -cp {jar_path} org.talkbank.chatter.App -inputFormat xml -outputFormat cha -output {output_path} {input_path}"

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        ## checks if there was a failure
        if output:
            pass
        if error:
            self.error_file

    ## create a text file with an error message if conversation fails
    def error_file(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT_ERROR
        )

        with io.open(path, "w", encoding="utf-8") as outfile:
            outfile.write("ERROR: CANNOT CONVERT TO CHAT FILE")
