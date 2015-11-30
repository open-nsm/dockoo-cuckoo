from lib.cuckoo.common.abstracts import Machinery
from lib.cuckoo.common.exceptions import CuckooMachineError

class VirtualBox(Machinery):
    
    def _initialize_check(self):
        pass
        
    def start(self, label, task):     
        pass
       
    def stop(self, label):
        pass
                    
    def _list(self):
        machines = ["NA"]
        return machines
    
    def _status(self, label):
        return "Still working on status"
    

    def dump_memory(self, label, path):
        pass
    
                              