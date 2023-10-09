import requests
import streamlit as st
import json

st.title("Orca Chatbot")


st.sidebar.image("imgs\majestic-orca.png")
st.sidebar.header("Configuration")


# Endpoint selection
selected_endpoint = st.sidebar.selectbox("Select the API endpoint:", ["/orca/system-chat", "/orca/qa"])

# UI and logic for /orca/system-chat
if selected_endpoint == "/orca/system-chat":
    st.subheader("System-User Chat")
    
    system_prompt = st.text_input('System Prompt:', 'Hello, how can I assist you today?')
    user_prompt = st.text_input('User Prompt:', 'Tell me a joke.')
    
    if st.button('Send to /orca/system-chat'):
        payload = {
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }
        try:
            response = requests.post('http://localhost:8000/orca/system-chat', json=payload)
            response.raise_for_status()
            orca_response = response.json()['orca-response']
            st.write(f'**Assistant:** {orca_response}')
        except requests.RequestException as e:
            st.write(f'An error occurred: {e}')

# UI and logic for /orca/qa
elif selected_endpoint == "/orca/qa":
    st.subheader("Question-Answering Endpoint")
    
    # UI elements for the /orca/qa endpoint
    input_text = st.text_area('Input Text:', 'Type your question or text here.')
    
    if st.button('Send to /orca/qa'):
        headers = {'Content-Type': 'application/json'}
        payload = {'input_text': input_text}
        
        try:
            response = requests.post('http://localhost:8000/orca/qa', json=payload, headers=headers)
            response.raise_for_status()
            orca_response = response.json().get('orca-response', 'No response key found.')
            st.write(f'**Response:** {orca_response}')
        except requests.RequestException as e:
            st.write(f'An error occurred: {e}')





