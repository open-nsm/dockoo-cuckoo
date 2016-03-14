import datetime
import logging
import os.path
import json
import re
import subprocess
import importlib

from modules.processing import output_parse

from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.exceptions import CuckooProcessingError
from lib.cuckoo.common.constants import CUCKOO_ROOT
from lib.cuckoo.common.config import Config

log = logging.getLogger(__name__)
# This class will return results for Docker analysis
class Dockerproc(Processing):

    def run(self):
        self.key = "dockerproc"

        self.options_docker = Config(file_name="docker-mach")

        # Retrieve results from appropriate directory
        # print (self.analysis_path)

        # Which docker containers were supposed to run?
        docker_images = self.task['docker_images']
        file_processed = os.path.split(self.task['target'])[1]
        time_stamp = str(self.task['completed_on'])

        # List of containers finding suspicious results
        suspicious_results = []

        # Dictionary of results
        results_dictionary = {}

        docker_image_list = (self.task['docker_images']).split(',')
        for docker_tool in docker_image_list:
            input_file = os.path.join(CUCKOO_ROOT, "storage", "analyses",str(self.task['id']),docker_tool)



            parser = eval('self.options_docker' + '.' + docker_tool + '[\'output_parser\']')
            #function_to_call = 'output_parse.' + parser + '.' + 'testfunc(\'hello\')'
            parser_function = ('output_parse.' + parser + '.' + 'parsefile(\''\
                + input_file + '\')')
            print(parser_function)
            json_results = eval(parser_function)
            # insert results into results dictionary with docker_tool as key
            results_dictionary[docker_tool] = json.loads(json_results)

            # Check to see whether output shows suspicious results
            suspect_function = ('output_parse.' + parser + '.' + 'suspicious(\''\
                + input_file + '\')')
            suspicious = eval(suspect_function)
            # If result is suspicious, add to list
            if (suspicious):
                suspicious_results.append(docker_tool)


        summary = "No suspicious results found"
        if (len(suspicious_results) > 0):
            summary = "Suspicious results found in " + ",".join(suspicious_results)
        #parser_file = os.path.join(CUCKOO_ROOT,'modules','processing', (self.options_docker['output_parser']) + '.py')
        #print(parser_file)
        results = {
            "summary": summary,
            "docker_image": docker_images,
            "file_processed": file_processed,
            "timestamp": time_stamp,
            "result": results_dictionary,
        }

        return results