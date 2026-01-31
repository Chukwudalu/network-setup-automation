import subprocess
import shlex
import uuid
import os
import abc


vboxmanage = "vboxmanage"


class Operation(metaclass=abc.ABCMeta):
    def __init__(self, desc, vm, cmd):
        self.desc = desc
        self.vm = vm
        self.cmd = cmd

    @abc.abstractmethod
    def execute(self):
        pass

class Run(Operation):
    def execute(self):
        guest_cmd_split = shlex.split(self.cmd)
        command = subprocess.run(
            [
                vboxmanage,
                'guestcontrol',
                self.vm,
                'run',
                '--username',
                'root',
                '--password',
                'P@ssw0rd',
                '--',
                *guest_cmd_split
            ],
            text=True,
            stdout=subprocess.PIPE
        )

        return command.stdout

    def execute_script(self, script):
        with open(f"scripts/{script}", 'r', encoding="utf-8") as f:
            data = f.read()

        data = data.replace("\r\n", "\n")

        command = subprocess.run(
            [
                "VBoxManage",
                "guestcontrol",
                self.vm,
                "run",
                "--username", "root",
                "--password", "P@ssw0rd",
                "--exe", "/bin/bash",
                "--",
                "-c",
                data,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )
        return command.stdout + command.stderr
    



class RunVboxManage():
    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self):
        cmd = shlex.split(self.cmd)
        command = subprocess.run(
            [
                vboxmanage,
                *cmd
            ],
            text=True,
            stdout=subprocess.PIPE
        )
        return command.stdout


