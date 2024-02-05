#!/bin/bash


sudo apt update
sudo apt -y upgrade
sudo apt-get -y install --reinstall raspberrypi-bootloader raspberrypi-kernel
sudo apt-get -y install raspberrypi-kernel-headers

echo "connect <NI USB GPIB Calbe>"
echo "update pi finish, do <sudo reboot>"
