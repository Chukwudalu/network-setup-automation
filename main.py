import argparse
import time
from rich.panel import Panel
from rich.progress import track
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Column, Table
import sys
import signal
import tasks

def sigint_handler(signum, frame):
    print("\nSIGINT captured. Bye!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


console = Console()

def run():
    parser = argparse.ArgumentParser(prog='Network Setup',description='This script is designed to automate the setup of a virtual network in virtual box')

    parser.add_argument('-t', '--task',
                        choices=['list_vms', 'enter_vm'])

    parser.add_argument('-v', '--vm')
    
    parser.add_argument('-c', '--clone')

    args = parser.parse_args()

    if args.clone is not None and (args.task is not None or args.vm is not None):
        parser.error("--clone cannot have additional flags")


    if args.task == "enter_vm" and args.vm is None:
        parser.error("--vm required when using -t enter_vm")

    if args.vm and args.task is None:
        parser.error("-t required when using -v ")

    match args.task:
        case "list_vms":
            names = tasks.list_machines()
            list_view_table = Table("Machines")
            for name in names:
                list_view_table.add_row(name)
            console.print(list_view_table)

        case "enter_vm":
            if args.vm in tasks.list_machines():
                enter_vm(args.vm)
            else:
                print("Machine Not avaliable")

    if args.clone is not None:
        clone(args.clone)


def clone(name):
    try:
        for i in track(range(5), description="clonning...."):
            time.sleep(1)
    except:
        pass

    tasks.createvm(name)


def enter_vm(vm):
    print(f"Entering {vm}. Enter `quit` to exit")
    while True:
        print("0. run scripts")
        print("1. list interfaces")
        print("2. rename interfaces")
        print("3: Sanity")
        
        print("q: to quit")
        user_input = input("Enter task: ")
        if user_input == "quit" or user_input == "q":
            break
        
        print('\n')
        match user_input:
            case '1':
                raw = tasks.list_ifaces(vm)
                syntax = Syntax(raw, "text", theme="ansi_dark")
                console.print(Panel(syntax, title="Network Interfaces", border_style="cyan"))
            case '0':
                tasks.show_scripts()
                script = input("Enter script name to execute: ")
                output = tasks.execute_custom_script(script, vm)
                syntax = Syntax(output, "text", theme="ansi_dark")
                console.print(Panel(syntax, title=f"{script}", border_style="bright_red"))
            case '2':
                try:
                    cmd = tasks.execute_custom_script('iface_rename.sh', vm)
                    syntax = Syntax(cmd, "text", theme="ansi_dark")
                    console.print(Panel(syntax, title=f"Renaming iface name to device name", border_style="bright_red"))
                except:
                    print('iface_rename.sh required')
            case '3':
                try:
                    cmd = tasks.execute_custom_script('sanity.sh', vm)
                    syntax = Syntax(cmd, "text", theme="ansi_dark")
                    console.print(Panel(syntax, title=f"Sanity", border_style="bright_red"))
                except:
                    print('sanity.sh required')
                    
                                


if __name__ == "__main__":
    run()
