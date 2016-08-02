import os, json, sys
import paramiko
import shutil
import subprocess
import time

"""
project strings to pass to rpiDBUploader:
- apdflash
- ghosts
- common

"""

class rpiDBUploader():
    def __init__(self, filepath, project):

        self.ssh = paramiko.SSHClient()
        self.filepath = filepath
        self.project = project

        robinIP = "192.168.2.188"
        username = "robin"
        password = "freeasinfreedom"
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.projects = {
            "apdflash": "Hsin\ Yee\ [SRP]",
            "ghosts": "GhostImaging",
            "common": "Common"
        }

        self.ssh.connect(robinIP, username = username, password = password)

    def upload(self):
        # hard coded lmao
        shutil.copy(self.filepath, os.path.join("/mnt/photonics", self.filepath))
        self.uploadFromNFS()

    def uploadFromNFS(self):
        c = 0
        while 1:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("ls /mnt/photonics | grep {}".format(self.filepath))
            stdout = ssh_stdout.readlines()[0].strip()
            if stdout == self.filepath:
                print("running cp -r -v /mnt/photonics/{0} /home/robin/Dropbox/hbar/{1}/".format(self.filepath, self.projects[self.project]))
                ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("cp -r -v /mnt/photonics/{0} /home/robin/Dropbox/hbar/{1}/ > /home/robin/Dropbox/hbar/{1}/rpiDBUploader.log".format(self.filepath, self.projects[self.project]))
                try:
                    print(ssh_stdout.readline())
                    print(ssh_stderr.readline())
                except:
                    pass
                print("Uploaded successfully! Exiting...")
                break
            else:
                time.sleep(1)
                print("Waiting... ")
                c += 1
                if c > 20:
                    print("Timeout after 20 seconds. Attempt to upload failed. Quitting")

#c = rpiDBUploader("apdflash20151214_1004.tar.gz", "apdflash")
#c.upload()
