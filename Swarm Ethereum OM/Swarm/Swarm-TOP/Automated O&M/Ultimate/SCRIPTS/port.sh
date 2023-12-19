#!/bin/bash
cd /usr/local/script
sudo rm /usr/local/ports.txt
sudo touch /usr/local/script/ports.txt
echo "$(sudo docker ps | grep eth | grep bee | awk -F '-' '{print $1}' | awk -F ':' '{print $3+2}')" > ports.txt