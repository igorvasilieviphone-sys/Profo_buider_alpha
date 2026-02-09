# backend/main.py
import os
import sys

# Настройка прокси для Psiphon (обязательно в самом верху)
PSIPHON_PORT = "10809" 
os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{PSIPHON_PORT}'
os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{PSIPHON_PORT}'

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import json
import sqlite3
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from chat import get_gemini_response
import random
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if os.path.exists(DOTENV_PATH):
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    load_dotenv()

try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    # Конфигурация: transport='rest' критически важен для работы через Psiphon
    genai.configure(api_key=api_key, transport='rest')
    
    EMBEDDING_MODEL = 'text-embedding-004'
    # Используем полное имя модели
    ANALYSIS_MODEL = genai.GenerativeModel('gemini-2.5-flash')
    logging.info("Gemini AI services configured successfully (REST mode).")
except Exception as e:
    logging.error(f"Failed to configure Gemini AI: {e}")
    genai = ANALYSIS_MODEL = None

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        return None

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_query_embedding(text):
    if not genai: return None
    try:
        result = genai.embed_content(model=EMBEDDING_MODEL, content=text, task_type="RETRIEVAL_QUERY")
        return np.array(result['embedding'])
    except Exception as e:
        logging.error(f"Embedding error: {e}")
        return None

def analyze_user_text_for_rules(text: str) -> dict:
    if not ANALYSIS_MODEL: return {"positive_summary": text, "exclusion_keywords": []}
    prompt = (
        "Ты — эксперт-профориентолог. Твоя задача — проанализировать текст пользователя и вернуть ТОЛЬКО валидный JSON-объект со структурой "
        "{\"positive_summary\": \"string\", \"exclusion_keywords\": [\"string\"]}.\n"
        f"Текст пользователя: '{text}'"
    )
    try:
        response = ANALYSIS_MODEL.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        logging.error(f"Analysis error: {e}")
        return {"positive_summary": text, "exclusion_keywords": []}

@app.route('/')
def index(): return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename): return send_from_directory(PROJECT_ROOT, filename)

@app.route('/api/chat', methods=['POST'])
def handle_chat_message():
    data = request.get_json()
    user_message = data.get('message')
    if not user_message: return jsonify({'error': 'No message'}), 400
    ai_response_text = get_gemini_response(user_message)
    return jsonify({'response': ai_response_text})

@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not ANALYSIS_MODEL: return jsonify({"error": "AI service is unavailable."}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '').strip()

        analysis = analyze_user_text_for_rules(additional_info) if additional_info else {"positive_summary": "", "exclusion_keywords": []}
        
        conn = get_db_connection()
        # ... (здесь остается твоя логика поиска по базе careers.db, она верная)
        # Для краткости я не дублирую блок SQL, оставь его как был в твоем коде
        conn.close()
        return jsonify([]) # Замени на возврат списка final_careers
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)