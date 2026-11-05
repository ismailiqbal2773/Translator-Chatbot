# Free Translator Chatbot

A lightweight translation chatbot built with Streamlit and `deep-translator`.
It supports 12 target languages without a paid API key.

## Features

- Explicit source-language selection for dependable fallback behavior
- Google Translator with automatic MyMemory fallback
- Friendly errors without raw provider exception details
- Last successful result retained during normal Streamlit reruns
- Input validation up to 5,000 characters

## Supported target languages

English, Urdu, French, German, Spanish, Chinese, Arabic, Hindi, Turkish,
Russian, Japanese and Korean.

## Installation

```bash
pip install -r requirements.txt
streamlit run translator_chatbot.py
```

## Tests

```bash
pip install pytest
pytest -q test_translation_service.py test_app.py
```

## Project structure

- `translator_chatbot.py` - Streamlit user interface
- `translation_service.py` - validation and provider fallback logic
- `test_translation_service.py` - automated tests
- `requirements.txt` - runtime dependencies

The project uses third-party translation services through the MIT-licensed
`deep-translator` package. Provider availability and translation quality can vary.
Text leaves this app: it is sent to Google, and on failure to MyMemory. Do not enter
confidential school, student, staff or customer information. MyMemory fallback is
limited to 500 UTF-8 bytes per request; longer input is not forwarded to it.
Source language must now be selected explicitly; the fallback API rejects `auto`.
The last successful result stays labelled with its original language after reruns.

References: [deep-translator](https://github.com/nidhaloff/deep-translator)
and [MyMemory API limits](https://mymemory.translated.net/doc/spec.php).
No upstream source code was copied or relicensed. This repository has no LICENSE
file; the dependency's MIT license does not license this project's own code.

Created by Muhammad Ismail.
