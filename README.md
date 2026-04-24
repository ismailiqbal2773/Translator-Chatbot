**Free Translator Chatbot**

A lightweight translation chatbot built with Streamlit and Google Translator. This application provides a clean user interface for translating text between 12 different languages without requiring any paid API keys.

**Features**

Auto Detection: Automatically detects the source language of the input text.

Multi-Language Support: Supports 12 languages including English, Urdu, French, German, Spanish, Chinese, Arabic, Hindi, Turkish, Russian, Japanese, and Korean.

No API Keys: Uses free translation libraries; no setup or paid keys required.

Minimal UI: Clean and distraction-free user interface built with Streamlit.

**Tech Stack**

Frontend: Streamlit

Backend: Python

Translation Engine: Google Translator (via deep_translator library)

**Installation**

Follow these steps to set up the project locally.

**Clone the repository**

git clone https://github.com/ismailiqbal2773/Translator-Chatbot.git

cd Translator-Chatbot

**Install dependencies**

pip install -r requirements.txt

**Run the application**

streamlit run translator_chatbot.py

**Usage**

Enter or paste the text you want to translate in the input field.

Select the target language from the dropdown menu.

Click the Translate button to view the result.

**Project Structure**

translator-chatbot/

├── translator_chatbot.py   # Main application script

├── requirements.txt        # Project dependencies

└── README.md               # Project documentation


