import os
import whisper
from gtts import gTTS
import io
import streamlit as st
from pyngrok import ngrok
from streamlit_chat import message
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import audio_recorder_streamlit as ars
import nltk

from 
# import pyttsx3

# Download the necessary NLTK data
nltk.download('wordnet')

# Load the Whisper model
model = whisper.load_model("base")

# Initialize the converter
# engine = pyttsx3.init()

# Initialize conversation history and state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_state' not in st.session_state:
    st.session_state.current_state = "start"

# Streamlit UI elements
st.title("English Speaking Practice App")

# Welcome message
if st.session_state.current_state == "start":
    st.write("Hi! How would you like to practice your English speaking?")
    # Convert text to speech
    # engine.say("Hi! How would you like to practice your English speaking?")
    # engine.runAndWait()
    option = st.selectbox(
        "Choose an option:",
        ["Conversation practice", "Pronunciation", "Vocabulary"]
    )

    if st.button("Start"):
        st.session_state.current_state = option.lower().replace(" ", "_")
        st.session_state.conversation_history = []
        st.session_state.user_input = ""
        st.session_state.bot_response = ""
    
    st.write("Great! Let's start with a conversation practice session.")
    st.write("Enter your message in the text box below.")

    # Text input for user message
    user_text = st.text_input("Your message:", "")

    if st.button("Check"):
        if user_text:
            try:
                # Add user input to conversation history
                st.session_state.conversation_history.append({"role": "user", "content": user_text})

                # Call the function from the other Python file
                response_message = some_module.process_text(user_text)
                st.session_state.conversation_history.append({"role": "assistant", "content": response_message})

                # Display conversation history
                for chat in st.session_state.conversation_history:
                    is_user = chat["role"] == "user"
                    st.write(f"{'You' if is_user else 'Assistant'}: {chat['content']}")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.button("End Conversation"):
        st.write("Thank you for the conversation practice! Here's your feedback: [Feedback based on user's input]")
        st.session_state.current_state = "start"
# if st.session_state.current_state == "conversation_practice":
#     st.write("Great! Let's start with a conversation practice session.")
#     st.write("Record your message using the button below.")
    
#     # Capture audio input from the microphone
#     audio_data = ars.audio_recorder()

#     if audio_data:
#         try:
#             # Convert audio data to a format Whisper can process
#             audio = whisper.load_audio(io.BytesIO(audio_data))
            
#             # Transcribe the audio using Whisper
#             result = model.transcribe(audio)
#             user_text = result["text"]

#             # Add user input to conversation history
#             st.session_state.conversation_history.append({"role": "user", "content": user_text})

#             # Generate a response using a hypothetical model
#             response_message = "Thank you for sharing! Here's some feedback: [Feedback based on user's input]"
#             st.session_state.conversation_history.append({"role": "assistant", "content": response_message})

#             # Display conversation history
#             for chat in st.session_state.conversation_history:
#                 message(chat["content"], is_user=chat["role"] == "user")

#             # Convert the response text to speech
#             tts = gTTS(response_message)
#             response_audio_io = io.BytesIO()
#             tts.write_to_fp(response_audio_io)
#             response_audio_io.seek(0)

#             st.audio(response_audio_io, format='audio/mp3')

#         except Exception as e:
#             st.error(f"An error occurred: {e}")

#     if st.button("End Conversation"):
#         st.write("Thank you for the conversation practice! Here's your feedback: [Feedback based on user's input]")
#         st.session_state.current_state = "start"

elif st.session_state.current_state == "pronunciation":
    word = st.text_input("Enter a word to pronounce:")
    if st.button("Pronounce"):
        try:
            tts = gTTS(word)
            response_audio_io = io.BytesIO()
            tts.write_to_fp(response_audio_io)
            response_audio_io.seek(0)
            st.audio(response_audio_io, format='audio/mp3')
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif st.session_state.current_state == "vocabulary":
    word = st.text_input("Enter a word to get synonyms:")
    if st.button("Get Synonyms"):
        try:
            synonyms = wordnet.synsets(word)
            english_synonyms = set()
            translator = GoogleTranslator(source='en', target='ur')

            for syn in synonyms:
                for lemma in syn.lemmas():
                    english_synonyms.add(lemma.name())

            # Translate synonyms to Urdu
            urdu_synonyms = [translator.translate(word) for word in english_synonyms]

            st.write(f"English Synonyms: {', '.join(english_synonyms)}")
            st.write(f"Urdu Synonyms: {', '.join(urdu_synonyms)}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
