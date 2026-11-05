from dataclasses import dataclass

from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import RequestError, TooManyRequests


GOOGLE_LANGUAGE_CODES = {
    "English": "en", "Urdu": "ur", "French": "fr", "German": "de",
    "Spanish": "es", "Chinese": "zh-CN", "Arabic": "ar", "Hindi": "hi",
    "Turkish": "tr", "Russian": "ru", "Japanese": "ja", "Korean": "ko",
}

MYMEMORY_LANGUAGE_CODES = {
    "English": "en-GB", "Urdu": "ur-PK", "French": "fr-FR",
    "German": "de-DE", "Spanish": "es-ES", "Chinese": "zh-CN",
    "Arabic": "ar-SA", "Hindi": "hi-IN", "Turkish": "tr-TR",
    "Russian": "ru-RU", "Japanese": "ja-JP", "Korean": "ko-KR",
}


class TranslationUnavailable(Exception):
    """Raised when both free translation providers are unavailable."""


@dataclass(frozen=True)
class TranslationResult:
    text: str
    provider: str
    used_fallback: bool


def validate_text(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Please enter text to translate.")
    if len(cleaned) > 5000:
        raise ValueError("Please keep the text under 5,000 characters.")
    return cleaned


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResult:
    cleaned = validate_text(text)
    if source_language not in GOOGLE_LANGUAGE_CODES or target_language not in GOOGLE_LANGUAGE_CODES:
        raise ValueError("Please select supported source and target languages.")
    if source_language == target_language:
        raise ValueError("Please select two different languages.")

    try:
        translated = GoogleTranslator(
            source=GOOGLE_LANGUAGE_CODES[source_language],
            target=GOOGLE_LANGUAGE_CODES[target_language],
        ).translate(cleaned)
        return TranslationResult(translated, "Google Translator", False)
    except (TooManyRequests, RequestError):
        pass
    except Exception:
        pass

    if len(cleaned.encode("utf-8")) > 500:
        raise TranslationUnavailable(
            "The primary service is unavailable. The fallback supports up to 500 UTF-8 bytes; shorten the text and try again."
        )

    try:
        translated = MyMemoryTranslator(
            source=MYMEMORY_LANGUAGE_CODES[source_language],
            target=MYMEMORY_LANGUAGE_CODES[target_language],
        ).translate(cleaned)
        return TranslationResult(translated, "MyMemory", True)
    except Exception as exc:
        raise TranslationUnavailable(
            "Translation services are temporarily unavailable. Please try again shortly."
        ) from exc
