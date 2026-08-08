
import streamlit as st
from TTS.api import TTS
import os
VOICE_DIR = "voices"

def get_voice_list():
    if not os.path.exists(VOICE_DIR):
        os.makedirs(VOICE_DIR)
    return [f for f in os.listdir(VOICE_DIR) if f.endswith(".wav")]

# load external CSS (clean way)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(BASE_DIR, "ui", "style.css")

with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Voice Cloning", page_icon="🎙️")

st.title("🎙️Personal Voice Cloning System for Content Creation")
col1, col2 = st.columns(2)
#col1 - voice library , col2 - language selection
with col1:
    st.subheader("🎙️ Voice Library")

    voice_files = get_voice_list()
    if voice_files:
        selected_voice = st.selectbox("Select Voice", voice_files)
    else:
        selected_voice = None
        st.warning("Upload a voice first.")

    uploaded_file = st.file_uploader("Upload Voice (.wav)", type=["wav"])
    if uploaded_file is not None:
        save_path = os.path.join(VOICE_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Voice '{uploaded_file.name}' added!")



# fixed paths (same as  CLI)
REFERENCE_WAV = os.path.join(VOICE_DIR, selected_voice)
OUTPUT_WAV = "test_output.wav"
# 🌍 Language Selection (SAFE VERSION)
with col2:
    st.subheader("🌍 Language Selection")

    language_options = {
        "English": "en",
        "French": "fr-fr",
        "Portuguese": "pt-br"
    }

    selected_language_name = st.selectbox(
        "Select Language",
        list(language_options.keys())
    )

    LANGUAGE = language_options[selected_language_name]
# text input
text = st.text_area(
    "Enter text to Clone with your voice",
    height=150,
    placeholder="Hello. My name is Paras Bhatt from Raipur."
)

@st.cache_resource
def load_tts():
    return TTS(
        model_name="tts_models/multilingual/multi-dataset/your_tts"
    )

tts = load_tts()

if st.button("Generate Speech"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    elif selected_voice == "No voices available":
        st.error("Please upload a voice first.")
    else:
        with st.spinner("Generating speech..."):
            tts.tts_to_file(
                text=text,
                speaker_wav=REFERENCE_WAV,
                language=LANGUAGE,
                file_path=OUTPUT_WAV
            )
        st.success("Speech generated successfully!")
        st.audio(OUTPUT_WAV)
