#!/bin/bash
  
cd /usr/local/script
sudo rm addr.txt
sudo touch addr.txt
prefix=0x
deined_dirnames=$(sudo find / -type f -name "swarm.key" -path "*swarm*" | xargs dirname)

addrfiles=$(sudo find / -type f -name "swarm.key" -path "*swarm*")
for deined_dirname in $deined_dirnames;
    do sudo chmod 777 $deined_dirname
done

for addrfile in $addrfiles;do
    un_addrs=$(sudo cat $addrfile)
    addrs=$(echo $prefix${un_addrs: 12: 40})
    echo "$addrs" 
done > addr.txt
