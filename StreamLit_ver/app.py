import nltk
from components import show_sidebar
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import torch
import torch.nn as nn
import json
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load environment variables
load_dotenv()
groq_api = os.getenv('groq_api')
if not groq_api:
    st.error("Groq API key is missing in the environment variables.")
    exit()

client = Groq(api_key=groq_api)

# Set page config
st.set_page_config(
    page_title="HealthCare Assistant",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# Load intents
with open("intents.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Data Preprocessing
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

# Stem and sort words
words = [stemmer.stem(w.lower()) for w in words if w not in ["?", "!", ".", ","]]
words = sorted(list(set(words)))
labels = sorted(labels)

# Neural network model definition
class ChatNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChatNet, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.softmax(self.layer3(x))
        return x

# Helper functions for model training and inference
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for s_word in s_words:
        for i, w in enumerate(words):
            if w == s_word:
                bag[i] = 1
    
    return np.array(bag)

def prepare_training_data():
    training = []
    output = []
    
    for i, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = [0 for _ in range(len(labels))]
        output_row[labels.index(docs_y[i])] = 1

        training.append(bag)
        output.append(output_row)

    return np.array(training), np.array(output)

def create_model(training_data, output_data):
    input_size = len(training_data[0])
    hidden_size = 8
    output_size = len(output_data[0])
    
    model = ChatNet(input_size, hidden_size, output_size)
    
    # Define loss and optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Training the model
    epochs = 1000
    for epoch in range(epochs):
        # Convert data to tensors
        x = torch.FloatTensor(training_data)
        y = torch.FloatTensor(output_data)
        
        # Forward pass
        outputs = model(x)
        loss = criterion(outputs, y)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # Save the trained model
    torch.save(model.state_dict(), "model.pth")
    
    return model

def analyze_health_from_text(text):
    try:
        # Check if it's a greeting
        greeting_words = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        is_greeting = any(greeting in text.lower() for greeting in greeting_words)

        if is_greeting:
            return "Hello! How can I assist you with your health concerns today?"
        else:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"As a healthcare assistant, provide medical advice for: {text}. Be concise but thorough. Include any relevant medical information and quick remedies if applicable."
                }],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I couldn't process your request at the moment. Error: {str(e)}"

# Basic chat interface
def chat(model):
    # Initialize session state variables
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Add a session state to track the message processing
    if 'message_processed' not in st.session_state:
        st.session_state.message_processed = False
        
    # Show sidebar
    show_sidebar()
    
    # Apply enhanced styling for a professional, full-width chat interface
    st.markdown("""
        <style>
            /* Import professional fonts */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Work+Sans:wght@300;400;500;600;700&display=swap');
            
            /* Base styling with professional gradient background */
            body {
                background: linear-gradient(120deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                width: 100vw;
            }
            
            .stApp {
                background: linear-gradient(120deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
                color: white;
                font-family: 'Roboto', 'Work Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            
            /* Remove unwanted elements */
            .css-1kyxreq, .css-zt5igj, .css-qrbaxs {display: none !important;}
            
            /* Full-width design elements */
            .main .block-container {
                max-width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            
            /* Full-width header with professional styling */
            .chat-header {
                text-align: center;
                margin: 0;
                padding: 30px 0;
                width: 100%;
                background: linear-gradient(90deg, rgba(20,76,99,0.9) 0%, rgba(23,107,135,0.9) 50%, rgba(20,76,99,0.9) 100%);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }
            
            .chat-header h1 {
                color: white;
                font-family: 'Work Sans', 'Roboto', sans-serif;
                font-size: 2.8rem;
                font-weight: 600;
                letter-spacing: -0.5px;
                margin: 0;
                padding: 0;
                text-transform: none;
            }
            
            /* Message styling - professional gradients */
            .user-msg {
                background: linear-gradient(120deg, #2980b9 0%, #3498db 100%);
                color: white;
                padding: 14px 20px;
                border-radius: 18px 18px 4px 18px;
                margin: 15px 0;
                text-align: right;
                max-width: 75%;
                margin-left: auto;
                box-shadow: 0 4px 15px rgba(41, 128, 185, 0.2);
                word-break: break-word;
                position: relative;
                animation: slideInRight 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                font-family: 'Roboto', sans-serif;
                font-weight: 400;
            }
            
            .bot-msg {
                background: linear-gradient(120deg, #34495e 0%, #415b76 100%);
                color: #f0f0f0;
                padding: 14px 20px;
                border-radius: 18px 18px 18px 4px;
                margin: 15px 0;
                text-align: left;
                max-width: 75%;
                margin-right: auto;
                box-shadow: 0 4px 15px rgba(52, 73, 94, 0.2);
                word-break: break-word;
                position: relative;
                animation: slideInLeft 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                font-family: 'Roboto', sans-serif;
                font-weight: 400;
            }
            
            /* Content area */
            .chat-content-area {
                padding: 20px 5%;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            /* Fix emoji placement */
            .user-icon {
                margin-right: 10px;
                font-size: 1.2rem;
                order: -1;
            }
            
            .bot-icon {
                margin-right: 10px;
                font-size: 1.2rem;
                order: -1;
            }
            
            /* Message content wrapper */
            .msg-content {
                flex: 1;
            }
            
            /* Animations */
            @keyframes slideInRight {
                from { opacity: 0; transform: translateX(30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            /* Professional form styling */
            .stForm {
                background: rgba(52, 73, 94, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px !important;
                padding: 20px !important;
                margin-top: 20px !important;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
                max-width: 1400px;
                margin-left: auto;
                margin-right: auto;
            }
            
            /* Make text fields look professional */
            .stTextInput > div > div > input {
                background: rgba(255, 255, 255, 0.08) !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 8px !important;
                padding: 16px 20px !important;
                font-size: 16px !important;
                font-family: 'Roboto', sans-serif !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #3498db !important;
                box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3) !important;
                background: rgba(255, 255, 255, 0.12) !important;
            }
            
            /* Button styling */
            .stButton button {
                background: linear-gradient(90deg, #2980b9 0%, #3498db 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 24px !important;
                font-weight: 500 !important;
                font-family: 'Roboto', sans-serif !important;
                transition: all 0.3s ease !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .stButton button:hover {
                background: linear-gradient(90deg, #2573a7 0%, #2980b9 100%) !important;
                box-shadow: 0 6px 15px rgba(41, 128, 185, 0.3) !important;
                transform: translateY(-2px) !important;
            }
            
            /* Scrollbar styling */
            .main::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            .main::-webkit-scrollbar-track {
                background: rgba(30, 30, 30, 0.2);
                border-radius: 10px;
            }
            
            .main::-webkit-scrollbar-thumb {
                background: rgba(52, 152, 219, 0.7);
                border-radius: 10px;
                border: 2px solid rgba(30, 30, 30, 0.2);
            }
            
            .main::-webkit-scrollbar-thumb:hover {
                background: rgba(41, 128, 185, 0.9);
            }
            
            /* Responsive adjustment */
            @media (max-width: 768px) {
                .user-msg, .bot-msg {
                    max-width: 85%;
                    padding: 12px 16px;
                }
                
                .chat-header h1 {
                    font-size: 2rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Full-width header
    st.markdown('<div class="chat-header"><h1>Healthcare Assistant</h1></div>', unsafe_allow_html=True)
    
    # Content area
    st.markdown('<div class="chat-content-area">', unsafe_allow_html=True)
    
    # Display chat messages using standard Streamlit components
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown(
                f"""<div class='bot-msg'>
                    <span class='bot-icon'>🤖</span>
                    <div class='msg-content'>Hello! How can I assist you with your health concerns today?</div>
                </div>""", 
                unsafe_allow_html=True
            )
            
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f"""<div class='user-msg'>
                        <span class='user-icon'>👤</span>
                        <div class='msg-content'>{message['content']}</div>
                    </div>""", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""<div class='bot-msg'>
                        <span class='bot-icon'>🤖</span>
                        <div class='msg-content'>{message['content']}</div>
                    </div>""", 
                    unsafe_allow_html=True
                )
    
    # Close content area
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input field in a form
    with st.form(key="message_form", clear_on_submit=True):
        # Create columns inside the form
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Message", 
                placeholder="Type your health-related question here...", 
                label_visibility="collapsed",
                key="input_field"
            )
            
        with col2:
            submit_button = st.form_submit_button("Send")
        
        # Process user input only on form submission
        if submit_button and user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate response
            with st.spinner(""):
                response = analyze_health_from_text(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Flag that we've processed this message
            st.session_state.message_processed = True
            st.rerun()

# Main function
def main():
    input_size = len(words)
    hidden_size = 8
    output_size = len(labels)
    model = ChatNet(input_size, hidden_size, output_size)
    
    if os.path.exists("model.pth"):
        model.load_state_dict(torch.load("model.pth"))
    else:
        training_data, output_data = prepare_training_data()
        model = create_model(training_data, output_data)

    chat(model)

# Run the Streamlit App
if __name__ == "__main__":
    main()
