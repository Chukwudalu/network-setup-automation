#!/usr/bin/bash

# List all interfaces with MAC, IPv4, IPv6
ip -o link show | while read -r idx name rest; do
  # name comes like "eth0:" -> strip trailing colon
  name=${name%:}

  # Get MAC from the same line (link/ether <MAC> ...)
  mac=$(echo "$rest" | awk '{
        for (i = 1; i <= NF; i++) {
            if ($i == "link/ether") {
                print $(i + 1)
                break
            }
        }
    }')

  # Get IPv4 (may be empty)
  ipv4=$(ip -o -4 addr show dev "$name" | awk '{print $4}')
  # Get IPv6 (may be empty)
  ipv6=$(ip -o -6 addr show dev "$name" | awk '{print $4}')

  echo "Interface: $name"
  echo "  MAC:  ${mac:-"-"}"
  echo "  IPv4: ${ipv4:-"-"}"
  echo "  IPv6: ${ipv6:-"-"}"
  echo
done
