from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from translation_service import TranslationResult, TranslationUnavailable


def test_result_survives_language_change_and_failed_retry():
    app = AppTest.from_file("translator_chatbot.py").run()
    assert not app.exception
    app.text_area[0].set_value("Good morning")
    with patch("translation_service.translate_text", return_value=TranslationResult("صبح بخیر", "MyMemory", True)):
        app.button[0].click().run()
    assert app.success[0].value == "صبح بخیر"
    app.selectbox[1].select("French").run()
    assert app.success[0].value == "صبح بخیر"
    assert app.subheader[0].value == "Translation in Urdu"
    with patch("translation_service.translate_text", side_effect=TranslationUnavailable("Service unavailable")):
        app.button[0].click().run()
    assert app.error[0].value == "Service unavailable"
    assert app.success[0].value == "صبح بخیر"
    assert not app.exception
