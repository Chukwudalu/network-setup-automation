#!/bin/bash

nmcli connection modify "Wired connection 1" \
  ipv4.addresses "192.168.1.50/24" \
  ipv4.gateway "192.168.1.1" \
  ipv4.dns "8.8.8.8 1.1.1.1" \
  ipv4.method manual
