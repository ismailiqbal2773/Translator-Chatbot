import streamlit as st

from translation_service import (
    GOOGLE_LANGUAGE_CODES,
    TranslationUnavailable,
    translate_text,
)


st.set_page_config(page_title="Free Translator Chatbot", page_icon="🌍")
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(145deg, #f4f8f6 0%, #e8f1ed 100%); }
    .block-container { max-width: 820px; padding-top: 2.5rem; }
    h1 { color: #143c2e; letter-spacing: -0.03em; }
    [data-testid="stTextArea"] textarea { border-radius: 14px; }
    [data-testid="stButton"] button {
        border-radius: 12px; background: #176b4d; border: 0; font-weight: 700;
    }
    [data-testid="stAlert"] { border-radius: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🌍 Free Translator Chatbot")
st.caption("Translate short text with automatic provider fallback. No paid API key required.")
st.caption("Text is sent to Google and, if unavailable, MyMemory. Use non-confidential text only. Fallback limit: 500 UTF-8 bytes.")

if "last_translation" not in st.session_state:
    st.session_state.last_translation = None

text = st.text_area(
    "Enter text", height=150, max_chars=5000,
    placeholder="Type or paste text here...",
)
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("From", list(GOOGLE_LANGUAGE_CODES.keys()))
with col2:
    target = st.selectbox(
        "To", list(GOOGLE_LANGUAGE_CODES.keys()),
        index=list(GOOGLE_LANGUAGE_CODES.keys()).index("Urdu"),
    )

if st.button("Translate", type="primary", use_container_width=True):
    try:
        with st.spinner("Translating..."):
            result = translate_text(text, source, target)
        st.session_state.last_translation = {
            "source": source, "target": target, "text": result.text,
            "provider": result.provider, "used_fallback": result.used_fallback,
        }
    except ValueError as exc:
        st.warning(str(exc))
    except TranslationUnavailable as exc:
        st.error(str(exc))

last = st.session_state.last_translation
if last:
    st.subheader(f"Translation in {last['target']}")
    st.success(last["text"])
    if last["used_fallback"]:
        st.info("The primary provider was unavailable, so MyMemory completed this translation.")
    st.caption(f"Provider used: {last['provider']}")
