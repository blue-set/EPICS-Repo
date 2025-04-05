import nltk
import os
import sys

def ensure_nltk_resources():
    """Check and download necessary NLTK resources."""
    print("Checking NLTK resources...")
    
    # List of required NLTK resources for your application
    required_resources = [
        ('punkt', 'tokenizers/punkt'),
    ]
    
    for resource, path in required_resources:
        try:
            nltk.data.find(path)
            print(f"✓ {resource} is already downloaded")
        except LookupError:
            print(f"× {resource} not found, downloading...")
            nltk.download(resource)
            print(f"✓ {resource} has been downloaded")

    # Print NLTK data directories
    print("\nNLTK data directories:")
    for path in nltk.data.path:
        exists = "exists" if os.path.exists(path) else "does not exist"
        print(f"- {path} ({exists})")

if __name__ == "__main__":
    ensure_nltk_resources()
    print("\nScript completed. You can now run your application.")
