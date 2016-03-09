import docker
import ConfigParser
import time
import os
from os import path
import docker.tls as tls

from lib.cuckoo.common.abstracts import Machinery
from lib.cuckoo.common.exceptions import CuckooMachineError
from lib.cuckoo.common.constants import CUCKOO_ROOT


class VirtualBox(Machinery):
    def _initialize_check(self):
        pass

    def start(self, label, task):
        docker_images = self.options.get('docker-mach').get('images')
        docker_tasks = task.docker_images
        print docker_images
        print docker_tasks
        # Where is our input file?
        input_file = os.path.join(CUCKOO_ROOT, "storage", "analyses",
                                  str(task.id), "binary")
        print input_file

        # File to be analyzed
        # Dummy value -- need to track down symlink rep by input_file
        malware_file = "1d53a61b4ec187230f23fd66076ff605"

        # For now -- need to support comma-delimited multiple in future
        docker_tool = docker_tasks

        # Read in parameters from the config file

        container_name = self.options.pescanner.container_name
        local_working_dir = self.options.pescanner.local_working_dir
        #local_working_dir = os.path.join(CUCKOO_ROOT, "storage", "analyses",str(task.id))
        docker_bind_dir = self.options.pescanner.docker_bind_dir
        command_line_exe = self.options.pescanner.command_line_exe
        options = self.options.pescanner.options
        mode = self.options.pescanner.mode

        # Docker or docker-machine
        docker_exec = self.options.get('docker-mach').docker_exec

        # The command to run -- add options later?
        command2run = command_line_exe + " " + malware_file

        c = docker.Client()

        # Make a connection to docker
        if (docker_exec.lower() == 'docker'):
            c = docker.Client(base_url='unix://var/run/docker.sock')

        # Make a connection to docker-machine
        if (docker_exec.lower() == 'docker-machine'):
            ip_address = self.options.get('docker-mach').ip_address
            port = str(self.options.get('docker-mach').port)
            address_str = 'https://' + ip_address + ':' + port
            certs = self.options.get('docker-mach').cert_path
            tls_config = tls.TLSConfig(
                    client_cert=(path.join(certs, 'cert.pem'), path.join(certs, 'key.pem')),
                    ca_cert=path.join(certs, 'ca.pem'),
                    verify=True,
                    assert_hostname=False
            )
        c = docker.Client(base_url=address_str, tls=tls_config)

        # Grab the image
        c.images(container_name)

        host_config=c.create_host_config(binds={
            local_working_dir: {
                'bind': docker_bind_dir,
                'mode': mode,
            }
        })

        # Create a container based on parameters
        cntnr = c.create_container(
            container_name, command2run, volumes=[docker_bind_dir],
            host_config=host_config
        )

        # Start the container
        c.start(cntnr)

        # Wait for container to finish executing before accessing logs
        containers = c.containers()
        # For now, just see if there are any containers executing
        num_containers = len(containers)
        while (num_containers > 0):
            time.sleep(1)
            containers = c.containers()
            num_containers = len(containers)

        # Access output logs
        output = c.logs(cntnr)
        print(output)

    def stop(self, label):
        pass

    def _list(self):
        machines = ["NA"]
        return machines

    def _status(self, label):
        return "Still working on status"

    def dump_memory(self, label, path):
        pass
