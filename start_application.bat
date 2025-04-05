@echo off
echo Setting up environment for EPICS Health Chatbot...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using system Python.
)

REM Ensure NLTK resources are downloaded
echo Checking NLTK resources...
python check_nltk_resources.py

echo.
echo Starting application...
python backend\process_message.py
