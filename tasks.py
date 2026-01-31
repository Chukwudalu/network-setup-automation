from core import Run, RunVboxManage
import re, subprocess, os, pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree



vboxmanage = "vboxmanage"

def list_machines():
    """Display Running Virtual Machines"""
    cmd_out = RunVboxManage('list runningvms').execute()
    names = re.findall(r'"([^"]+)"', cmd_out)
    return names

def list_ifaces(vm: str):
    """"List the Interfaces in the virtual machine"""
    return Run('List Interface', vm, None).execute_script("show_iface.sh")
    
def execute_custom_script(name: str, vm: str):
    return Run(f'Running {name}', vm, None).execute_script(name)

def startvm(name: str):
    """Start Vm"""
    cmd = RunVboxManage(f'startvm {name} --type headless').execute()
    print("Clone Running")

def createvm(name: str):
    """
    Create a linked clone from base_vm_name@snapshot_name
    and register it under clone_name.
    """
    cmd = [
        "VBoxManage",
        "clonevm", "centos_8_base",
        "--snapshot", "clean_base",
        "--name", name,
        "--register",
        "--options", "link",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"clonevm failed ({result.returncode}):\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    print("Clone created successfully:")


def show_scripts():
    directory = os.path.abspath('scripts')
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="bold bright_blue",
    )
    walk_directory(pathlib.Path(directory), tree)
    print(tree)
    

def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)


