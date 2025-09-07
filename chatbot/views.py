import nltk
from nltk.tokenize import word_tokenize
import pyttsx3
from django.shortcuts import render
import speech_recognition as sr
import threading
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('wordnet')

r = sr.Recognizer()

lemmatizer = WordNetLemmatizer()
conversation_history = []

knowledge_base_file = 'ai_knowledge.txt'
with open(knowledge_base_file, 'r', encoding='utf-8') as f:
    knowledge_base = f.read()

abbreviation_pattern = r'([A-Za-z\s]+)\s+\(([A-Za-z0-9]+)\)'
abbreviation_map = {}
for match in re.finditer(abbreviation_pattern, knowledge_base):
    full_form = match.group(1).strip().lower()
    short_form = match.group(2).strip().lower()
    abbreviation_map[short_form] = full_form

for short_form, full_form in abbreviation_map.items():
    pattern = r'\b' + re.escape(short_form) + r'\b'
    knowledge_base = re.sub(pattern, full_form, knowledge_base, flags=re.IGNORECASE)

def lemmatize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    for short_form, full_form in abbreviation_map.items():
        pattern = r'\b' + re.escape(short_form) + r'\b'
        text = re.sub(pattern, full_form, text)
    words = word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(w) for w in words])

stop_phrases = [
    'what is', 'define', 'tell me about', 'explain', 'describe', 'give me', 'information about'
]

def clean_query(query):
    query = query.lower()
    query = re.sub(r'[^a-z0-9\s]', '', query)
    for phrase in stop_phrases:
        query = query.replace(phrase, '')
    return query.strip()

topic_pattern = r'\*\*(.*?)\*\*'
topic_headings = re.findall(topic_pattern, knowledge_base)
normalized_headings = {}
for h in topic_headings:
    h_no_paren = re.sub(r'\s*\(.*?\)\s*', '', h)
    normalized_headings[lemmatize_text(h_no_paren)] = h

subtopics = {}
topic_splits = re.split(r'\*\*(.*?)\*\*', knowledge_base)
for i in range(1, len(topic_splits), 2):
    heading = topic_splits[i].strip()
    content = topic_splits[i+1]
    subtopic_matches = list(re.finditer(r'^\s*(?:\d+\.\s+)?(.+?):\s*$', content, flags=re.MULTILINE))
    for j, m in enumerate(subtopic_matches):
        sub_name = m.group(1).strip()
        sub_name_no_paren = re.sub(r'\s*\(.*?\)\s*', '', sub_name)
        sub_norm = lemmatize_text(sub_name_no_paren)
        start = m.start()
        end = subtopic_matches[j+1].start() if j+1 < len(subtopic_matches) else len(content)
        sub_content = content[start:end].strip()
        subtopics[sub_norm] = sub_content

engine_lock = threading.Lock()

def speak(text):
    def run():
        engine = pyttsx3.init() 
        with engine_lock:
            engine.say(text)
            engine.runAndWait()
        engine.stop() 
    threading.Thread(target=run, daemon=True).start()


def get_response(query):
    query_cleaned = clean_query(query)
    lemmatized_query = lemmatize_text(query_cleaned)
    if lemmatized_query in ['ai', 'artificial intelligence', 'what is ai', 'define ai', 'introduction to ai']:
        section_pattern = r'(\*\*.*?\*\*.*?(?:ai refers to|artificial intelligence is).*?)(\*\*|$)'
        match = re.search(section_pattern, knowledge_base, flags=re.IGNORECASE | re.DOTALL)

        if match:
            section = match.group(1).strip()
            return section  
    for sub_norm in subtopics:
        if sub_norm in lemmatized_query:
            return subtopics[sub_norm]

    for topic_norm in normalized_headings:
        if topic_norm in lemmatized_query:
            heading_original = normalized_headings[topic_norm]
            pattern = re.escape(f"**{heading_original}**")
            match = re.search(pattern, knowledge_base)
            if match:
                start = match.start()
                next_topic_match = re.search(r'(^\d+\.\s\*\*|^\*\*.*?\*\*)', knowledge_base[match.end():], flags=re.MULTILINE)
                end = match.end() + (next_topic_match.start() if next_topic_match else len(knowledge_base))
                return knowledge_base[start:end].strip()

    return "Hmm… that’s interesting! But I’m only trained to talk about Artificial Intelligence. Try asking me about AI"

def chatbot(request):
    user_query = ''
    response = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        user_query = request.POST.get('query', '').strip()

        if action == 'speak' and not user_query:
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Listening…")
                    audio = r.listen(source)
                    user_query = r.recognize_google(audio)
            except Exception:
                response = "Voice recognition failed."
                conversation_history.append(('You', ''))
                conversation_history.append(('Bot', response))
                speak(response)
                return render(request, 'chatbot.html', {'response': response, 'conversation': conversation_history})

        if user_query:
            response = get_response(user_query)
        else:
            response = "Please type a query or use the microphone."

        conversation_history.append(('You' if action=='speak' else 'You', user_query))
        conversation_history.append(('Bot 🤖', response))

        if action == 'speak':
            speak(response)

    return render(request, 'chatbot.html', {'response': response, 'conversation': conversation_history})