import streamlit as st
import whisper
import pyaudio
import wave
import threading
import os
import numpy as np
import matplotlib.pyplot as plt

# Load the Whisper model
model = whisper.load_model("base")

# Parameters for recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize pyaudio
p = pyaudio.PyAudio()

# Flag to control recording
recording = False
frames = []

def record_audio():
    global recording, frames
    frames = []
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    st.write("Recording started...")

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    
    print(len(frames))
    stream.stop_stream()
    stream.close()
    st.write("Recording stopped.")

def start_recording():
    global recording
    recording = True
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()

def stop_recording():
    global recording
    recording = False
    p.terminate()
    st.write("Recording stopped.")

def save_audio_file(filename):
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        st.write(f"Audio saved to {filename}")
    except Exception as e:
        st.error(f"Error saving audio file: {e}")

def save_and_transcribe():
    save_audio_file(WAVE_OUTPUT_FILENAME)

    # Check if the file is empty
    if os.path.getsize(WAVE_OUTPUT_FILENAME) == 0:
        st.error("The recorded file is empty.")
        return "", None

    # Transcribe the audio file using Whisper
    try:
        result = model.transcribe(WAVE_OUTPUT_FILENAME)
        return result['text'], WAVE_OUTPUT_FILENAME
    except Exception as e:
        st.error(f"Error transcribing audio file: {e}")
        return "", None

def transcribe_uploaded_file(uploaded_file):
    temp_file_path = "temp_audio.wav"
    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        result = model.transcribe(temp_file_path)
        return result['text']
    except Exception as e:
        st.error(f"Error transcribing uploaded file: {e}")
        return ""
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Remove the file after transcription

st.title("Audio Recorder and Transcriber")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file is not None:
    st.write("Processing uploaded file...")
    transcription = transcribe_uploaded_file(uploaded_file)
    st.write("Transcription: ", transcription)

    # Provide a download button for the transcribed text with a unique key
    st.download_button(
        label="Download Transcription from Upload",
        data=transcription,
        file_name="transcription_from_upload.txt",
        mime="text/plain",
        key="download_upload"
    )

# Recording functionality
if st.button("Start Recording"):
    start_recording()

if st.button("Stop Recording"):
    stop_recording()

if st.button("Submit"):
    st.write("Transcribing...")
    transcription, recorded_file = save_and_transcribe()
    
    if transcription:
        st.write("Transcription: ", transcription)

        # Provide a download button for the transcribed text with a unique key
        st.download_button(
            label="Download Transcription from Recording",
            data=transcription,
            file_name="transcription_from_recording.txt",
            mime="text/plain",
            key="download_recording"
        )

        # Provide a download button for the recorded audio file with a unique key
        if recorded_file and os.path.exists(recorded_file):
            with open(recorded_file, "rb") as f:
                st.download_button(
                    label="Download Recorded Audio",
                    data=f,
                    file_name="recorded_audio.wav",
                    mime="audio/wav",
                    key="download_audio"
                )
            os.remove(recorded_file)  # Remove the file after downloading
        else:
            st.error("The recorded file is not available.")
    else:
        st.error("No transcription available. Please try recording again.")

# Button to save recorded audio file
if st.button("Save Recorded Audio"):
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        with open(WAVE_OUTPUT_FILENAME, "rb") as f:
            st.download_button(
                label="Download Saved Audio",
                data=f,
                file_name="saved_audio.wav",
                mime="audio/wav",
                key="download_saved_audio"
            )
    else:
        st.error("No recorded audio available to save.")

# Debugging: Display waveform of the recorded audio (if available)
if os.path.exists(WAVE_OUTPUT_FILENAME):
    try:
        with wave.open(WAVE_OUTPUT_FILENAME, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            plt.figure(figsize=(10, 4))
            plt.plot(audio_data)
            plt.title('Waveform of Recorded Audio')
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            st.pyplot(plt)
    except Exception as e:
        st.error(f"Error displaying waveform: {e}")
