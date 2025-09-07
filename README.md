# Ai_Chatbot
AI Chatbot built with Django, NLP, and speech recognition. Supports text and voice queries, retrieves AI knowledge from a structured knowledge base, and provides contextual responses.
# AI Chatbot - Django Web Application

An **AI-powered Chatbot** built using **Django**, designed to answer questions specifically about **Artificial Intelligence (AI)**.  
It supports **text input** and **voice input**, retrieves answers from a structured knowledge base, and speaks responses using text-to-speech (TTS).

---

## 🚀 Features

- Text-based and voice-based queries
- Handles abbreviations and maps short forms to full forms
- Retrieves answers based on **topics** and **subtopics**
- Text-to-Speech (TTS) for spoken responses
- Intelligent query processing using **lemmatization** and **stop phrase removal**
- Displays conversation history on the web interface
- Clean, simple UI with background image

---

## ⚙️ Technologies Used

- Python 3.x
- Django Web Framework
- NLTK (Natural Language Toolkit)
- scikit-learn
- pyttsx3 (Text-to-Speech)
- SpeechRecognition
- HTML/CSS

---

## ⚡ Installation & Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai-chatbot.git
    cd ai-chatbot
    ```

2. Run Django migrations:
    ```bash
    python manage.py migrate
    ```

3. Start the server:
    ```bash
    python manage.py runserver
    ```

4. Open your browser:
    ```
    http://127.0.0.1:8000/chatbot/
    ```

---

## ✅ Usage

- Type a question about AI in the input field and click **Ask**
- Or click **Speak** and ask a question using your microphone
- The chatbot responds with relevant answers and additional context
- Conversation history is displayed on the page
- Bot speaks responses when using voice input

---

## 🌟 How It Works

- The chatbot reads from a **knowledge base file** (`ai_knowledge.txt`)
- Abbreviations like "AI" are mapped to their full forms for accurate matching
- Queries are **lemmatized** and cleaned for better matching
- Responses are retrieved using **topic and subtopic detection**
- Text-to-speech responses are generated in a **separate thread** to avoid blocking the server

---

## 🌟 Acknowledgements

Inspired by advancements in **Artificial Intelligence (AI)**, **Natural Language Processing (NLP)**, and **conversational agents**.  
Special thanks to the open-source community for libraries like **Django**, **NLTK**, **pyttsx3**, and **SpeechRecognition**.

