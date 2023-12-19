#!/bin/bash
cd /usr/local/script
sudo touch dcdir.txt
echo "$(sudo find /swarm1 /swarm2 /swarm3 /swarm4 -mindepth 2 -type f -name "docker-compose.yaml"| grep -v "<anything you want to grep>"|grep -v "<anything you want to grep>")" > /usr/local/script/dcdir.txt

echo "$(sudo find /swarm4 -maxdepth 1 -type f -name "docker-compose.yaml"| grep -v "<anything you want to grep>"|grep -v "<anything you want to grep>" )" >> /usr/local/script/dcdir.txt