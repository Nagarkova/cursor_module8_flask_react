#!/bin/bash

# Stop Full-Stack Application Script

echo "Stopping application servers..."

if [ -f .app_pids ]; then
    PIDS=$(cat .app_pids)
    kill $PIDS 2>/dev/null
    rm .app_pids
    echo "Servers stopped"
else
    # Try to find and kill processes
    pkill -f "python3 app.py"
    pkill -f "react-scripts start"
    echo "Attempted to stop servers"
fi
