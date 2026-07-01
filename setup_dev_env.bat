@echo off
set VENV_DIR=.venv

echo Checking for virtual environment...
if not exist %VENV_DIR%\ (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Error: Failed to create virtual environment. Is Python installed and in your PATH?
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.

echo Installing project in editable mode...
pip install -e .
if errorlevel 1 (
    echo Error: Failed to install project dependencies.
    pause
    exit /b 1
)
echo Project installed in editable mode.

echo Development environment setup complete.
echo You are now in the virtual environment. To exit, type "deactivate".
echo To run your tests, navigate to the project root and run: python -m unittest discover tests
