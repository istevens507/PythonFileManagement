rem echo %cd%

echo off

set currentDirectory=%cd%

rem To activate a Python virtual environment named .venv,
call .venv\Scripts\activate.bat

cd %currentDirectory%\Helpers

py scriptStartup.py -scriptPath "%currentDirectory%\BusinessJobs"
pause