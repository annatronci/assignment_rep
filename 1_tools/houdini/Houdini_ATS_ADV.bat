@echo off

:: --- Define Houdini Script Root ---
set "SCRIPT_PATH=D:\ATS_QSYNC\Python Advanced\10_tools\assignment\houdini"

:: --- Use your custom Houdini user directory (forces pythonrc.py) ---
set "HOUDINI_USER_PREF_DIR=%SCRIPT_PATH%"

:: --- Add the script path and its parent to PYTHONPATH ---
set "PYTHONPATH=%SCRIPT_PATH%;%SCRIPT_PATH%\python3.11libs;%PYTHONPATH%"

:: --- HOUDINI SPLASHSCREEN  ---
set "HOUDINI_SPLASH_FILE=%SCRIPT_PATH%/img/houdinisplash.png"
set "HOUDINI_SPLASH_MESSAGE=HOUDINI FOR ATStudio"

:: --- Optional: Custom splash or message (won't affect startup unless manually handled) ---
set "HOUDINI_SPLASH_MESSAGE=HOUDINI FOR ATStudio"

:: --- Houdini binary ---
set "HOUDINI_DIR=C:\Program Files\Side Effects Software\Houdini 20.5.370\bin"
set "PATH=%PATH%;%HOUDINI_DIR%"

:: --- Launch Houdini ---
echo Launching Houdini...
houdinifx

pause

