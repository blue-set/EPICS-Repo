# Health_chatbot

Health Chatbot, which provides details of treatments and medicine details as per one's symptoms.

## Setup Instructions

1. Make sure you have Python 3.8+ installed
2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies and set up the environment:
   ```
   python setup.py
   ```
   
   Or install requirements manually:
   ```
   pip install -r requirements.txt
   python check_nltk_resources.py
   ```

4. Run the application using:
   ```
   python backend\process_message.py
   ```
