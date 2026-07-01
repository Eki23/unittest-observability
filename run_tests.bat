@echo off
set VENV_DIR=.venv

echo Setting up development environment and running tests...

rem Call the setup script to ensure venv is active and project is installed
call setup_dev_env.bat
if errorlevel 1 (
    echo Error during environment setup. Aborting test run.
    pause
    exit /b 1
)

echo Running all tests...
rem The venv should be active from setup_dev_env.bat
python -m unittest discover tests
if errorlevel 1 (
    echo Some tests failed.
) else (
    echo All tests passed.
)

echo Test run complete.
pause
