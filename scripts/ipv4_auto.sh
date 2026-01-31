#!/bin/bash
set -euo pipefail

CONN_NAME="enp0s3"

echo "Configuring '$CONN_NAME' for Automatic IPv4 (DHCP)..."

nmcli connection modify "$CONN_NAME" \
    ipv4.method auto \
    ipv4.addresses "" \
    ipv4.gateway "" \
    ipv4.dns ""

if nmcli connection up "$CONN_NAME"; then
    echo "Success: '$CONN_NAME' is now using DHCP."
else
    echo "Error: Failed to restart the connection."
    exit 1
fi
