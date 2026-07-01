@echo off
echo Running tests with coverage...

REM Activate virtual environment (adjust path if different)
call venv\Scripts\activate.bat

REM Run tests with coverage
coverage run -m unittest discover tests

REM Generate coverage report
coverage report -m

REM Deactivate virtual environment
call deactivate.bat

echo Coverage report generated.
pause
