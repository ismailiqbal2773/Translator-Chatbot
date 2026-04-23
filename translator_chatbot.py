import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Free Translator Chatbot")
st.title("🌍 Free Translator Chatbot")

# Languages you want to allow
LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh",
    "Arabic": "ar",
    "Hindi": "hi",
    "Turkish": "tr",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}

# Input
# text = st.text_input("Enter your text:")
text = st.text_area("Enter text")

target = st.selectbox("Translate to:", list(LANGUAGES.keys()))

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter text.")
    else:
        try:
            translated = GoogleTranslator(
                source='auto',
                target=LANGUAGES[target]
            ).translate(text) 
# source='auto' → Automatically detects input language
# target=LANGUAGES[target] → Converts selected language into code
# .translate(text) → Performs translation
            st.success(f"**Translated Text:** {translated}")

        except Exception as e:
            st.error(f"Error: {e}")
