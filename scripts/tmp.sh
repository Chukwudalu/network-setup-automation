#!/bin/bash

cat <<EOF > /etc/bird.conf

log syslog all;             # Log all messages

router id 10.20.30.100;     # use your routers enp0s3 IP as its ID R1

protocol device {           # the device "protocol" needs to be included to
                            # activate all of the interfaces
}

protocol kernel {
    ipv4 {                  # export all routes learned by bird to the kernel
          export all;       # routing table
    };
}

protocol ospf {            # Activate OSPF
    area 0 {
        interface "enp0s3" { # Configure the enp0s3 connected network to be
        };                   # advertised to other routers. Also send and receive
                             # link state advertisements on this interface

        interface "br0" { # Configure the enp0s8 connected network to be
            stub;            # to be advertised to other routers. Don't send or
        };                   # receive link stat advertisements on this interface
                             # accomplished by the "stub" directive
    };
}

EOF

sudo systemctl reload bird.service
sudo systemctl start bird.service
sudo systemctl enable bird.service
sudo systemctl status bird.service
