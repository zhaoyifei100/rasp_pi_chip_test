#!/bin/bash



if grep -q "DO NOT EDIT THIS FILE" /boot/config.txt; then
    sudo sed -i '/dtparam=i2c_arm=on/d' /boot/config.txt
    sudo sed -i '/dtparam=i2c_vc=on/d' /boot/config.txt
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
    echo "dtparam=i2c_vc=on" >> /boot/config.txt
    echo "arm_64bit=0" >> /boot/config.txt
else
    sudo sed -i '/dtparam=i2c_arm=on/d' /boot/firmware/config.txt
    sudo sed -i '/dtparam=i2c_vc=on/d' /boot/firmware/config.txt
    echo "dtparam=i2c_arm=on" >> /boot/firmware/config.txt
    echo "dtparam=i2c_vc=on" >> /boot/firmware/config.txt
    echo "arm_64bit=0" >> /boot/firmware/config.txt
fi
