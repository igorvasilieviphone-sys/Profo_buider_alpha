# backend/main.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import json
import sqlite3
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# --- ИМПОРТИРУЕМ ФУНКЦИЮ ЧАТА ИЗ chat.py ---
from chat import get_gemini_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Настройка путей ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if os.path.exists(DOTENV_PATH):
    load_dotenv(dotenv_path=DOTENV_PATH)
    logging.info(f"Loading environment variables from: {DOTENV_PATH}")
else:
    logging.warning(f".env file not found at: {DOTENV_PATH}. Attempting to use system-wide variables.")
    load_dotenv()

# --- Конфигурация Gemini (ТОЛЬКО для embeddings) ---
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    
    # В этом файле нам нужна только модель для векторов
    EMBEDDING_MODEL = 'models/text-embedding-004'
    logging.info("Gemini AI service for embeddings configured successfully.")

except (ValueError, KeyError, TypeError) as e:
    logging.error(f"Failed to configure Gemini AI for embeddings: {e}. Recommendation services may be disabled.")
    genai = None
    EMBEDDING_MODEL = None

app = Flask(__name__)
CORS(app)

# --- Функции для работы с БД (без изменений) ---
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

# --- Вспомогательные функции для работы с векторами (без изменений) ---
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_query_embedding(text):
    if not genai or not EMBEDDING_MODEL: return None
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="RETRIEVAL_QUERY"
        )
        return np.array(result['embedding'])
    except Exception as e:
        logging.error(f"Failed to get query embedding: {e}")
        return None

# --- Маршруты Flask ---
@app.route('/')
def index():
    return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(PROJECT_ROOT, filename)

# --- ИЗМЕНЕННЫЙ МАРШРУТ ЧАТА ---
@app.route('/api/chat', methods=['POST'])
def handle_chat_message():
    try:
        data = request.get_json()
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Просто вызываем функцию из chat.py. Вся логика "Профика" находится там.
        ai_response_text = get_gemini_response(user_message)
        
        return jsonify({'response': ai_response_text})
    except Exception as e:
        logging.error(f"Internal server error in handle_chat_message: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

# --- Маршрут для генерации карточек (без изменений) ---
@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not genai or not EMBEDDING_MODEL:
        return jsonify({"error": "AI service for recommendations is currently unavailable."}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '')
        if not selected_topics and not additional_info:
            return jsonify({'error': 'No topics or info provided'}), 400
        user_query = "Интересы пользователя: " + ", ".join(selected_topics)
        if additional_info:
            user_query += f". Дополнительная информация от пользователя: {additional_info}"
        logging.info(f"Processing user query for embeddings: {user_query}")
        query_embedding = get_query_embedding(user_query)
        if query_embedding is None:
            return jsonify({"error": "Could not process user query with AI."}), 500
        conn = get_db_connection()
        if conn is None: return jsonify({'error': 'DB connection failed'}), 500
        all_careers_cursor = conn.execute('SELECT * FROM careers WHERE embedding IS NOT NULL').fetchall()
        conn.close()
        if not all_careers_cursor:
            return jsonify({'error': 'No processed careers found in the database. Please run generate_embeddings.py first.'}), 500
        scored_careers = []
        for row in all_careers_cursor:
            career_data = dict(row)
            try:
                career_embedding = np.array(json.loads(career_data['embedding']))
                similarity = cosine_similarity(query_embedding, career_embedding)
                scored_careers.append((similarity, career_data))
            except (json.JSONDecodeError, TypeError):
                logging.warning(f"Could not parse embedding for career: {career_data.get('name')}")
                continue
        scored_careers.sort(key=lambda x: x[0], reverse=True)
        final_careers = []
        for score, career in scored_careers[:30]:
            del career['embedding']
            final_careers.append(career)
        return jsonify(final_careers)
    except Exception as e:
        logging.error(f"Critical error in generate_cards: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)