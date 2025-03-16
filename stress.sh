#!/bin/bash
while true; do
     echo "Starting stress test..."

    #cpu
    stress-ng --cpu 2 --timeout 30s &

    #i/o
    stress-ng --io 2 --timeout 30s &

    #memory
    stress-ng --vm 2 --vm-bytes 350M --timeout 30s &

    #disk_usage
    stress-ng --hdd 2 --timeout 30s &

    #network
    stress-ng --sock 2 --timeout 30s &

    wait
    echo "Stress test complete." 
    sleep 30
done
