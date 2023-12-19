#!/bin/bash
cd /usr/local/script
sudo touch dcdir.txt
echo "$(sudo find /swarm1 /swarm2 /swarm4 -type f -name "docker-compose.yaml"  -path "*swarm*" | grep -v "<anything you want to grep>"|grep -v "<anything you want to grep>")" > /usr/local/script/dcdir.txt