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

from Model_Conversation import correct_and_converse

# Download the necessary NLTK data
nltk.download('wordnet')

# Load the Whisper model
model = whisper.load_model("base")

# Initialize conversation history and state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_state' not in st.session_state:
    st.session_state.current_state = "start"

# Streamlit UI elements
st.title("English Learning Practice AI Bot")

# Sidebar for options
option = st.sidebar.selectbox(
    "Choose an option:",
    ["Conversation practice", "Pronunciation", "Vocabulary"]
)

if st.sidebar.button("Start"):
    st.session_state.current_state = option.lower().replace(" ", "_")
    st.session_state.conversation_history = []
    st.session_state.user_input = ""
    st.session_state.bot_response = ""

print(st.session_state.current_state)
# Main content based on the selected option
if st.session_state.current_state == "conversation_practice":
    # st.write("Hi! How would you like to practice your English speaking?")

    # st.write("Great! Let's start with a conversation practice session.")
    # st.write("Enter your message in the text box below.")

    # Text input for user message
    user_text = st.text_input("Your message:", "")

    if st.button("Check"):
        if user_text:
            try:
                # Add user input to conversation history
                st.session_state.conversation_history.append({"role": "user", "content": user_text})

                # Call the function from the other Python file
                response_message = correct_and_converse(user_text)
                st.session_state.conversation_history.append({"role": "assistant", "content": response_message})

                # Clear the text input
                st.session_state.user_text = ""

                # Display only the latest conversation message
                for chat in st.session_state.conversation_history:
                    if chat["role"] == "user":
                       
                        st.markdown(
                            f"""
                                <div style='text-align: right; margin-bottom: 10px;'>
                                    <div style='display: inline-block; background-color: #2f2f2f; padding: 10px; border-radius: 10px; max-width: 70%; margin-left: auto; text-align: left;'>
                                        {chat['content']}
                                    </div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style='text-align: left; margin-bottom: 10px;'>
                                <div style='display: inline-block; background-color: #2f2f2f; padding: 10px; border-radius: 10px; max-width: 70%;'>
                                    {chat['content']}
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )


                user_text = ""
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif st.session_state.current_state == "pronunciation":
    word = st.text_input("Enter your text to pronounce:")
    if st.button("Pronounce"):
        try:
            # Clear the text input
            user_text = ""
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
            # Clear the text input
            user_text = ""
            synonyms = wordnet.synsets(word)
            english_synonyms = set()
            translator = GoogleTranslator(source='en', target='ur')

            for syn in synonyms:
                for lemma in syn.lemmas():
                    english_synonyms.add(lemma.name())

            # Translate synonyms to Urdu
            urdu_synonyms = [translator.translate(word) for word in english_synonyms]

            st.write(f"English Synonyms: {', '.join(english_synonyms)}")
            st.write(f"Meaning in Urdu: {', '.join(urdu_synonyms)}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
