
@echo off

echo Getting toolkit path...
set TOOLKIT=D:\ATS-Drive\Python for DCC\week_9\assignment\scTouv_toolkit

echo Setting Houdini user folder...
set HOUDINI_USER_PREFS=%USERPROFILE%\Documents\houdini20.0

echo Setting environment variable for the tool...
set SC_TOUV_PATH=%TOOLKIT%\houdini_tool

echo Copying pythonrc.py...
copy /Y "%TOOLKIT%\startup\pythonrc.py" "%HOUDINI_USER_PREFS%\pythonrc.py"

echo Making sure toolbar folder exists...
if not exist "%HOUDINI_USER_PREFS%\toolbar" (
    mkdir "%HOUDINI_USER_PREFS%\toolbar"
)

echo Copying custom shelf file...
copy /Y "%TOOLKIT%\shelf\scTouv.shelf" "%HOUDINI_USER_PREFS%\toolbar\scTouv.shelf"

echo Starting Houdini...
start "" "C:\Program Files\Side Effects Software\Houdini 20.0.506\bin\houdini.exe"

