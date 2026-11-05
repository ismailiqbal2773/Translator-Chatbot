from unittest.mock import patch

import pytest
from deep_translator.exceptions import TooManyRequests

from translation_service import TranslationUnavailable, translate_text, validate_text


def test_validate_text_rejects_blank_input():
    with pytest.raises(ValueError, match="enter text"):
        validate_text("   ")


def test_validate_text_rejects_more_than_5000_characters():
    with pytest.raises(ValueError, match="5,000"):
        validate_text("a" * 5001)


@patch("translation_service.GoogleTranslator")
def test_primary_provider_success(google):
    google.return_value.translate.return_value = "Hola"
    result = translate_text("Hello", "English", "Spanish")
    assert (result.text, result.provider, result.used_fallback) == (
        "Hola", "Google Translator", False
    )


@patch("translation_service.MyMemoryTranslator")
@patch("translation_service.GoogleTranslator")
def test_rate_limit_uses_fallback(google, mymemory):
    google.return_value.translate.side_effect = TooManyRequests()
    mymemory.return_value.translate.return_value = "صبح بخیر"
    result = translate_text("Good morning", "English", "Urdu")
    assert (result.text, result.provider, result.used_fallback) == (
        "صبح بخیر", "MyMemory", True
    )


@patch("translation_service.MyMemoryTranslator")
@patch("translation_service.GoogleTranslator")
def test_both_providers_fail_with_friendly_error(google, mymemory):
    google.return_value.translate.side_effect = RuntimeError("provider detail")
    mymemory.return_value.translate.side_effect = RuntimeError("provider detail")
    with pytest.raises(TranslationUnavailable, match="temporarily unavailable"):
        translate_text("Hello", "English", "French")


def test_rejects_same_source_and_target_language():
    with pytest.raises(ValueError, match="different languages"):
        translate_text("Hello", "English", "English")


@patch("translation_service.MyMemoryTranslator")
@patch("translation_service.GoogleTranslator")
def test_oversized_utf8_input_is_not_forwarded_to_fallback(google, mymemory):
    google.return_value.translate.side_effect = TooManyRequests()
    with pytest.raises(TranslationUnavailable, match="500 UTF-8 bytes"):
        translate_text("ا" * 251, "Urdu", "English")
    mymemory.assert_not_called()
