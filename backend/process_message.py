#!/usr/bin/env python
# This script serves as a bridge between the Node.js server and the Python backend

import sys
import json
import os
import torch
import nltk
from dotenv import load_dotenv
from groq import Groq

# Add NLTK download at the beginning of the file
import nltk
# Make sure punkt is downloaded before any imports that might use it
nltk.download('punkt')

# Add parent directory to path to import existing modules
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# Fix the import path for components
# We need to temporarily modify sys.path to ensure StreamLit_ver.components is available
streamlit_dir = os.path.join(root_dir, 'StreamLit_ver')
sys.path.append(streamlit_dir)

# Set the working directory to StreamLit_ver to ensure relative file paths work
os.chdir(streamlit_dir)

# Make sure intents.json exists
intents_path = os.path.join(streamlit_dir, 'intents.json')
if not os.path.exists(intents_path):
    # Create a basic intents file if it doesn't exist
    sample_intents = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey", "How are you", "Greetings"],
                "responses": ["Hello! How can I assist you with your health today?"]
            },
            {
                "tag": "farewell",
                "patterns": ["Bye", "Goodbye", "See you", "Take care"],
                "responses": ["Goodbye! Take care of your health."]
            }
        ]
    }
    with open(intents_path, 'w', encoding='utf-8') as f:
        json.dump(sample_intents, f, indent=2)
    print(f"Created sample intents file at {intents_path}")

# Now we can import the analyze_health_from_text function
from StreamLit_ver.app import analyze_health_from_text

# Main function to process messages
def process_message():
    # Get message from command line argument
    if len(sys.argv) < 2:
        return json.dumps({"error": "No message provided"})
    
    message = sys.argv[1]
    
    try:
        # Call the existing analyze_health_from_text function
        response = analyze_health_from_text(message)
        return json.dumps({"message": response})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return json.dumps({
            "error": str(e),
            "details": error_details
        })

if __name__ == "__main__":
    result = process_message()
    print(result)