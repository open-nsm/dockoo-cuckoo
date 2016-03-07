from lib.cuckoo.common.abstracts import Machinery
from lib.cuckoo.common.exceptions import CuckooMachineError
from lib.cuckoo.common.constants import CUCKOO_ROOT
import os

class VirtualBox(Machinery):
    
    def _initialize_check(self):
        pass
        
    def start(self, label, task):
        docker_images = self.options.docker.images
        docker_tasks = task.docker_images
        print docker_images
        print docker_tasks
        # Where is our input file?
        input_file = os.path.join(CUCKOO_ROOT, "storage", "analyses",
                                      str(task.id), "binary")
        print input_file

       
    def stop(self, label):
        pass
                    
    def _list(self):
        machines = ["NA"]
        return machines
    
    def _status(self, label):
        return "Still working on status"
    

    def dump_memory(self, label, path):
        pass
    
                              