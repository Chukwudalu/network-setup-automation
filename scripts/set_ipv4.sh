#!/bin/bash

sudo nmcli con modify enp0s3 ipv4.addresses "172.26.20.34/27"
sudo nmcli con modify enp0s3 ipv4.gateway "172.26.20.1"
#sudo nmcli con modify enp0s3 ipv4.dns "8.8.8.8 1.1.1.1"
sudo nmcli con modify enp0s3 ipv4.method manual

sudo nmcli con down enp0s3
sudo nmcli con up enp0s3

echo "IF error try running iface_rename"
