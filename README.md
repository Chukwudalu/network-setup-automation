----
#Author: Jeremiah Okwuolisa
----

Script that manages virtual machines in virtual box, with the capability to insert custom scripts.


Custom scripts placed inside scripts/ directory

> cloned machines need to have guestadditions installed manually.


### Cloning
You must have your clone name to centos_8_base and create a snapshot called clean-base. Or just edit the tasks.py file.

### Usage
```bash
python3 main.py --help

python3 main.py -t list_vms

python3 main.py -t enter_vm -v r1

python3 main.py -c clone99
 
```

