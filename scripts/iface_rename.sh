#!/bin/bash

set -euo pipefail

# Get all devices that NetworkManager knows about
devices=$(nmcli -t -f DEVICE device status | grep -v '^$' | grep -v 'lo')

for dev in $devices; do
    # Get the connection currently bound to this device
    con=$(nmcli -t -f NAME,DEVICE connection show | grep ":$dev$" | cut -d: -f1)

    # If a connection exists, rename it to match the device name
    if [[ -n "$con" ]]; then
        echo "Renaming connection '$con' → '$dev'"
        nmcli connection modify "$con" connection.id "$dev"
    else
        # No connection exists; create one bound to this device
        echo "Creating new connection '$dev'"
        nmcli connection add type ethernet ifname "$dev" con-name "$dev"
    fi
done
