import datetime
import logging
import os.path
import re
import subprocess

from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.exceptions import CuckooProcessingError

log = logging.getLogger(__name__)

# This class will return results for Docker analysis
class Dockerproc(Processing):
    
    def run(self):
        self.key = "dockerproc"
        # TODO Fill this in with real results
        # Retrieve results from appropriate directory
        print (self.analysis_path)
        # Which docker containers were supposed to run?
        print (self.task['docker_images'])
        results = {
            "summary": "docker not yet implemented",
            "docker_image": "N/A",
            "file_processed": "N/A",
            "timestamp": None,
            "result": "N/A",
        }
        
        return results   