import pyttsx3
import speech_recognition as sr
import torch
import streamlit as st
import random
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from datasets import load_dataset


@st.cache_resource # Store model and dataset in cache
def load(): # Load model
    tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b")
    model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True)

def generateAnimation(text):
    newText = ""
    for chunk in text.split():
        newText += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(newText + "▌")
    return newText

def generateSpeech(text):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id) # Sets voice
    engine.setProperty('rate', 170) # Changes the speed of the voice
    engine.setProperty('volume',1.0) # Setting up volume level between 0 and 1
    engine.say(text)
    engine.runAndWait() 

def transcribeSpeech():
    r = sr.Recognizer()   
    with sr.Microphone() as source: # Using mic for input
        r.adjust_for_ambient_noise(source, duration=1) # Wait for a sec to let recognizer adjust the energy threshold based on the surrounding noise level
        with st.spinner("Listening..."):
            audio = r.listen(source) # Listen for user's input
            userInput = r.recognize_google(audio) # Using google to recognize audio
            userInput = userInput.lower()
            return userInput

load()
# Setting page title and header
st.title("Ask Dolly :robot_face:")
SpeechText = ""
#STT
if speak_button := st.button("Speak", key="speak"):
    SpeechText = transcribeSpeech()
    SpeechText += "?"
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": SpeechText})
    

# Clearing conversation
if clear_button := st.button("Clear Conversation", key="clear"):
    st.session_state.messages = []
    st.session_state['messages'] = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    st.session_state['dolly_model'] = []

# Initialise session state variables
if "dolly_model" not in st.session_state:
    st.session_state["dolly_model"] = "databricks/dolly-v2-3b"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("Send a message"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Generate and display assistant response if no messages in chat history
if not st.session_state.messages:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! I am Dolly! How can I assist you today?",
                "Hi human! I'm Dolly! Is there anything I can help you with?",
                "Greetings! The name's Dolly! Do you need help?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        full_response = generateAnimation(assistant_response)
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    generateSpeech(full_response)
else:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True)
        mainText = prompt if not SpeechText else SpeechText
        res = generate_text(mainText)
        full_response = res[0]["generated_text"]
        animatedResponse = generateAnimation(full_response)
        message_placeholder.markdown(animatedResponse)
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    generateSpeech(full_response)

