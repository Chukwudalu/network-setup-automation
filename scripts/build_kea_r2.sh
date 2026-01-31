#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root (e.g., with sudo)." >&2
    exit 1
fi

echo "You are Fucked!!!"

cat << EOF > /etc/kea/kea-dhcp4.conf
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": [ "enp0s8" ]
    },

    "expired-leases-processing": {
      "reclaim-timer-wait-time": 10,
      "flush-reclaimed-timer-wait-time": 25,
      "hold-reclaimed-time": 3600,
      "max-reclaim-leases": 100,
      "max-reclaim-time": 250,
      "unwarned-reclaim-cycles": 5
    },

    "control-socket": {
      "socket-type": "unix",
      "socket-name": "kea4-ctrl-socket"
    },

    "renew-timer": 900,
    "rebind-timer": 1800,
    "valid-lifetime": 3600,

    "lease-database": {
      "type": "memfile"
    },


    "subnet4": [
      {
        "id": 1,
        "subnet": "172.26.20.32/27",
        "pools": [
          {
            "pool": "172.26.20.34-172.26.20.62"
          }
        ],
        "reservations": [
          {
            "hw-address": "08:00:27:d7:67:b5",
            "ip-address": "172.26.20.34"
          }
        ],
        "option-data": [
          {
            "name": "routers",
            "data": "172.26.20.33"
          }
        ]
      }
    ],

    // --- LOGGING ---
    "loggers": [
        {
            "name": "kea-dhcp4",
            "output_options": [
                {
                    "output": "stdout"
                }
            ],
            "severity": "DEBUG"
        }
    ]
  }

}
EOF

sudo systemctl start kea-dhcp4 

sudo systemctl reload kea-dhcp4

sudo systemctl enable kea-dhcp4



