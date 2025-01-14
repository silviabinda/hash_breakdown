#!/bin/bash

while true; do
    /usr/bin/python3 /home/silvia-pi/Desktop/double_pir.py # Replace with path to the double_pir.py code
    exit_status=$?
    if [ $exit_status -eq 0 ]; then
        echo "Script exited normally"
        break
    else
        echo "Script failed with status $exit_status. Restarting..."
        sleep 1  # Optional: Prevents spamming restarts immediately
    fi
done
