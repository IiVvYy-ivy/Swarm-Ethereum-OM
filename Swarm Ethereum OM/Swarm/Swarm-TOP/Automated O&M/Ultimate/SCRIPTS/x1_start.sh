#!/bin/bash    
dirnames=($(sudo find /swarm1 /swarm2 /swarm3 /swarm4 -mindepth 2 -type f -name "docker-compose.yaml"| grep -v "<anything you want to grep>"|grep -v "<anything you want to grep>" | xargs dirname && sudo find /swarm4 -maxdepth 1 -type f -name "docker-compose.yaml"| grep -v "<anything you want to grep>"|grep -v "<anything you want to grep>" |xargs dirname)) 
echo "dir should be dealt with :" 
counter=0  
for dirname in "${dirnames[@]}"  
do  
    echo "[$counter]$dirname"
    counter=$((counter+1))  
done  

echo
echo

# 询问是否需要继续执行脚本    
read -p "Countinue Script? (yes/no) " answer 

if [ "$answer" != "yes" ]; then    
  exit 0    
fi    
    
while true
do
   counter=0  
   for dirname in "${dirnames[@]}"  
   do  
       echo "[$counter]$dirname"
       counter=$((counter+1))  
   done
   echo  
   read -p "Which directory?(1/2/3...) " dir 
   cd "${dirnames[$dir]}" 
   sed -n '61p;81p' .env
   sudo docker-compose down
   sleep 15
   sudo docker-compose up -d
   sleep 15
   sudo chown -R systemd-coredump:systemd-coredump bee*
   sleep 1
   echo
   read -p "Countinue Script? (yes/no) " input
   if [ "$input" = "yes" ]; then
       continue
   else
       break
    fi
done