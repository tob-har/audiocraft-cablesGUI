#!/bin/bash

# Navigate to the first directory and run the script
cd /Users/tobias.hartmann/Documents/audiocraft-main-cablesUI
python serverCables.py &

# Wait a few seconds to ensure the above script starts properly
sleep 12

# Navigate to the second directory and run the http.server
cd /Users/tobias.hartmann/Documents/audiocraft-main-cablesUI/cables_audiocraftAPI4
python -m http.server & 