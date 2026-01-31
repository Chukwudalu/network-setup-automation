#!/bin/bash

cat <<EOF >/etc/sysctl.conf

net.ipv4.ip_forward = 1

EOF

sudo sysctl --system
