import subprocess
import sys
import os

def setup_environment():
    """Set up the environment for the EPICS application."""
    print("Setting up environment for EPICS application...")
    
    # Install requirements
    print("Installing requirements from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run the NLTK resource checker
    print("\nChecking NLTK resources...")
    subprocess.check_call([sys.executable, "check_nltk_resources.py"])
    
    print("\nSetup complete! You can now run the application.")

if __name__ == "__main__":
    setup_environment()
