#!/bin/bash

while true; do
    /usr/bin/python3 /home/silvia-pi/Desktop/main_code.py # Replace with the path to the main code
    exit_status=$?
    if [ $exit_status -eq 0 ]; then
        echo "Script exited normally"
        break
    else
        echo "Script failed with status $exit_status. Restarting..."
        sleep 1  # Optional: Prevents spamming restarts immediately
    fi
done
