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
    def run(self, structure_interact_instance):
        input_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.NATIVE_XML
        )

        output_path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT
        )

        jar_path = structure_interact_instance.chatter_path

        command = f"java -cp {jar_path} org.talkbank.chatter.App -inputFormat xml -outputFormat cha -output {output_path} {input_path}"

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if output:
            pass
        if error:
            self.error_file

    def error_file(self, structure_interact_instance):
        path = os.path.join(
            structure_interact_instance.output_path, OUTPUT_FILE.CHAT_ERROR
        )

        ## Creates the path where the text file will be written
        with io.open(path, "w", encoding="utf-8") as outfile:
            outfile.write("ERROR: CANNOT CONVERT TO CHAT FILE")
