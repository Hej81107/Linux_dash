#!/bin/bash

# Kill any existing VNC sessions
vncserver -kill :1 2>/dev/null || echo "No existing VNC server running on :1"

# Start a new VNC server session
vncserver :1 -geometry 1280x800 -depth 24

echo "VNC server started on display :1"
