import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h2 style='color: #10a37f;'>HealthCare Assistant</h2>
                <p style='color: #a8a8a8;'>Your AI-powered medical companion</p>
            </div>
            
            <div style='padding: 20px; background: #1a1b1e; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #ffffff;'>Features</h3>
                <ul style='color: #a8a8a8; list-style-type: none; padding-left: 0;'>
                    <li style='margin: 10px 0;'>🏥 <span style='margin-left: 8px;'>Medical Information</span></li>
                    <li style='margin: 10px 0;'>💊 <span style='margin-left: 8px;'>Treatment Suggestions</span></li>
                    <li style='margin: 10px 0;'>🩺 <span style='margin-left: 8px;'>Health Advice</span></li>
                    <li style='margin: 10px 0;'>❓ <span style='margin-left: 8px;'>Medical Queries</span></li>
                </ul>
            </div>
            
            <div style='padding: 20px; background: #1a1b1e; border-radius: 10px; margin: 10px 0;'>
                <h3 style='color: #ffffff;'>Disclaimer</h3>
                <p style='color: #a8a8a8; font-size: 0.9em;'>
                    This AI assistant provides general information only. Always consult a healthcare professional for medical advice.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Single clear chat button
        if st.button("Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_input = ""
            st.rerun() 