#!/bin/bash

sudo nmcli con delete enp0s9
sudo nmcli con delete enp0s8

sudo nmcli connection add type bridge ifname br0 con-name br0

sudo nmcli connection add type bridge-slave ifname enp0s8 master br0 con-name br0-slave-enp0s8
sudo nmcli connection add type bridge-slave ifname enp0s9 master br0 con-name br0-slave-enp0s9

sudo nmcli connection modify br0 ipv4.addresses "192.168.100.1/24"
sudo nmcli connection modify br0 ipv4.method manual

sudo nmcli connection up br0
sudo nmcli connection up br0-slave-enp0s8
sudo nmcli connection up br0-slave-enp0s9
