#!/bin/bash
while true; do
     echo "Starting stress test..."

    #Cpu test
    stress-ng --cpu 2 --timeout 30s

    #I/o
    stress-ng --io 2 --timeout 30s

    #Memory test
    stress-ng --vm 2 --vm-bytes 350M --timeout 30s

    #Disk_usage
    stress-ng --hdd 2 --timeout 30s

    #Network
    stress-ng --sock 2 --timeout 30s

    wait
    sleep 30
done
