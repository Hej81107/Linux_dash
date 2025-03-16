#!/bin/bash
while true; do
     echo "Starting stress test..."
    
    # CPU Stress (2 workers for 30s)
    stress-ng --cpu 2 --timeout 30s &

    # IO Stress (2 workers for 30s)
    stress-ng --io 2 --timeout 30s &

    # Memory Stress (2 workers, 256MB each for 30s)
    stress-ng --vm 2 --vm-bytes 400M --timeout 30s &

    # Filesystem Stress (2 workers for 30s)
    stress-ng --hdd 2 --timeout 30s &

    # Network Stress (2 workers for 30s)
    stress-ng --sock 2 --timeout 30s &

    wait
    echo "Stress test complete." 
done
