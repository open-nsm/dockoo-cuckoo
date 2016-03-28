import docker
import ConfigParser
import time
import os
from os import path
import shutil
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
        # This is our input file, but it's a symlink
        input_file = os.path.join(CUCKOO_ROOT, "storage", "analyses",
                                  str(task.id), "binary")

        # Name of file stored in storage binaries that symlink points to
        malware_file = os.path.basename(os.path.realpath(input_file))

        # malware_file is a very long string, and at least one Docker
        # container (Mastiff) doesn't like it.  So hence this workaround

        # create temporary file in binaries directory
        tmpdir = CUCKOO_ROOT +  "/storage/binaries/" + str(task.id)
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)

        # Get the original name of the file
        (targpath,orig_file_name) = os.path.split(task.target)

        # The full path of malware_file
        too_long_filename = os.path.realpath(input_file)

        # copy malware_file binary to temp directory
        shutil.move(too_long_filename,tmpdir)

        # rename malware_file to (shorter) original file name
        os.rename(tmpdir + '/' + malware_file, tmpdir + '/' + orig_file_name)

        # For now -- need to support comma-delimited multiple in future
        docker_task_list = docker_tasks.split(',')
        for docker_tool in docker_task_list:
            #docker_tool = docker_tasks

            # Read in parameters from the config file

            container_name = self.options.get(docker_tool).container_name

            #local_working_dir = os.path.join(CUCKOO_ROOT, "storage", "binaries")
            # Use temporary directory with shorter filename as the share
            local_working_dir = tmpdir
            # Get values from config file
            docker_bind_dir = self.options.get(docker_tool).docker_bind_dir
            command_line_exe = self.options.get(docker_tool).command_line_exe
            options = self.options.get(docker_tool).options
            mode = self.options.get(docker_tool).mode

            # Docker or docker-machine
            docker_exec = self.options.get('docker-mach').docker_exec

            # The command to run -- add options later?
            #command2run = command_line_exe + " " + docker_bind_dir + "/" + malware_file
            # Command to run with original filename
            command2run = command_line_exe + " " + docker_bind_dir + "/" + orig_file_name

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
            # TODO Better check to see whether analysis has stopped
            num_containers = len(containers)
            while (num_containers > 0):
                time.sleep(1)
                containers = c.containers()
                num_containers = len(containers)

            # Access output logs
            output = c.logs(cntnr)
            print(output)
            # file to store results
            storage_file = os.path.join(CUCKOO_ROOT, "storage", "analyses",str(task.id),docker_tool)
            f = open(storage_file, 'w')
            f.write(output)

        # Clean up temp directory
        shutil.rmtree(tmpdir)

    def stop(self, label):
        pass

    def _list(self):
        machines = ["NA"]
        return machines

    def _status(self, label):
        return "Still working on status"

    def dump_memory(self, label, path):
        pass
