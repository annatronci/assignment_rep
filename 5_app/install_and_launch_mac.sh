#!/bin/bash

# Percorso del tuo toolkit
TOOLKIT_DIR="/Volumes/ATS_QSYNC/assignment_rep/5_app/scTouv_toolkit"

# Variabili Houdini
export HOUDINI_PATH="$TOOLKIT_DIR:&"

# Menu interattivo
echo "Which version of Houdini do you want to run?"
echo "1) Houdini 20.5.654"
echo "2) Houdini 21.0.440"
read -p "Select (1 o 2): " choice

if [ "$choice" == "1" ]; then
    HOUDINI_BIN="/Applications/Houdini/Houdini20.5.654/Frameworks/Houdini.framework/Versions/Current/Resources/bin/houdini"
elif [ "$choice" == "2" ]; then
    HOUDINI_BIN="/Applications/Houdini/Houdini21.0.440/Frameworks/Houdini.framework/Versions/Current/Resources/bin/houdini"
else
    echo "Invalid choice."
    exit 1
fi

# Avvia Houdini
"$HOUDINI_BIN" &
