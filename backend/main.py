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
    logging.info(f"Loading environment variables from: {DOTENV_PATH}")
else:
    logging.warning(f".env file not found at: {DOTENV_PATH}. Attempting to use system-wide variables.")
    load_dotenv()

try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    EMBEDDING_MODEL = 'models/text-embedding-004'
    ANALYSIS_MODEL = genai.GenerativeModel('gemini-2.5-flash')
    logging.info("Gemini AI services configured successfully.")
except (ValueError, KeyError, TypeError) as e:
    logging.error(f"Failed to configure Gemini AI: {e}. Services may be disabled.")
    genai = None
    EMBEDDING_MODEL = None
    ANALYSIS_MODEL = None

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

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

def analyze_user_text_for_rules(text: str) -> dict:
    if not ANALYSIS_MODEL:
        return {"positive_summary": text, "exclusion_keywords": []}

    prompt = (
        "Ты — эксперт-профориентолог. Твоя задача — проанализировать текст пользователя и вернуть ТОЛЬКО валидный JSON-объект со структурой "
        "{\"positive_summary\": \"string\", \"exclusion_keywords\": [\"string\"]}.\n"
        "- 'positive_summary': Краткое саммари того, что пользователь ХОЧЕТ. Если позитивных пожеланий нет, оставь строку пустой.\n"
        "- 'exclusion_keywords': Это САМОЕ ВАЖНОЕ. Ты должен создать ИСЧЕРПЫВАЮЩИЙ список ключевых слов в нижнем регистре для сфер, которые пользователь КАТЕГОРИЧЕСКИ НЕ ХОЧЕТ. "
        "Когда ты находишь категорию (например, 'IT' или 'медицина'), ты ОБЯЗАН включить в список все возможные синонимы, связанные профессии и технологии. Будь максимально подробным.\n\n"
        "ПРИМЕР:\n"
        "Текст пользователя: 'Я гуманитарий, ненавижу IT и все, что связано с кодом. Ненавижу продажи.'\n"
        "Твой ОБЯЗАТЕЛЬНЫЙ ответ:\n"
        "{\n"
        "  \"positive_summary\": \"Пользователь ищет работу в гуманитарной сфере.\",\n"
        "  \"exclusion_keywords\": [\"it\", \"программирование\", \"код\", \"разработчик\", \"data science\", \"аналитик данных\", \"data scientist\", \"ml\", \"machine learning\", \"devops\", \"тестировщик\", \"qa\", \"продажи\", \"менеджер по продажам\", \"crm\"]\n"
        "}\n\n"
        "ТЕПЕРЬ ПРОАНАЛИЗИРУЙ ЭТОТ ТЕКСТ:\n"
        f"Текст пользователя: '{text}'"
    )
    
    try:
        response = ANALYSIS_MODEL.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        analysis_result = json.loads(cleaned_response)
        logging.info(f"AI analysis result: {analysis_result}")
        return analysis_result
    except (Exception, json.JSONDecodeError) as e:
        logging.error(f"Failed to analyze user text or parse JSON: {e}")
        return {"positive_summary": text, "exclusion_keywords": []}

@app.route('/')
def index():
    return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(PROJECT_ROOT, filename)

@app.route('/api/chat', methods=['POST'])
def handle_chat_message():
    try:
        data = request.get_json()
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        ai_response_text = get_gemini_response(user_message)
        return jsonify({'response': ai_response_text})
    except Exception as e:
        logging.error(f"Internal server error: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not genai or not EMBEDDING_MODEL:
        return jsonify({"error": "AI service is unavailable."}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '').strip()

        if not selected_topics and not additional_info:
            return jsonify({'error': 'No topics or info provided'}), 400

        analysis = {"positive_summary": "", "exclusion_keywords": []}
        if additional_info:
            analysis = analyze_user_text_for_rules(additional_info)
        
        positive_summary = analysis.get("positive_summary", "").strip()
        exclusion_keywords = analysis.get("exclusion_keywords", [])
        
        has_positive_info = bool(selected_topics) or bool(positive_summary)

        all_careers_raw = []
        conn = get_db_connection()
        if conn is None: return jsonify({'error': 'DB connection failed'}), 500
        
        if has_positive_info:
            logging.info("Mode: Vector Search + Filtering")
            selected_topics_text = ", ".join(selected_topics)
            user_query = f"Интересы: {selected_topics_text}. Пожелания: {positive_summary}"
            logging.info(f"Processing vector query: {user_query}")
            
            query_embedding = get_query_embedding(user_query)
            if query_embedding is None: return jsonify({"error": "Could not process query."}), 500

            all_careers_cursor = conn.execute('SELECT * FROM careers WHERE embedding IS NOT NULL').fetchall()
            
            scored_careers = []
            for row in all_careers_cursor:
                career_data = dict(row)
                try:
                    career_embedding = np.array(json.loads(career_data['embedding']))
                    similarity = cosine_similarity(query_embedding, career_embedding)
                    scored_careers.append((similarity, career_data))
                except (json.JSONDecodeError, TypeError): continue
            
            scored_careers.sort(key=lambda x: x[0], reverse=True)
            all_careers_raw = [career for score, career in scored_careers]

        else:
            logging.info("Mode: Filter-Only (no positive info provided)")
            all_careers_cursor = conn.execute('SELECT * FROM careers').fetchall()
            all_careers_raw = [dict(row) for row in all_careers_cursor]
            random.shuffle(all_careers_raw)

        conn.close()

        final_careers = []
        for career in all_careers_raw:
            if len(final_careers) >= 50: break

            is_excluded = False
            if exclusion_keywords:
                career_name_lower = career['name'].lower()
                career_industry_lower = career['industry'].lower()
                for keyword in exclusion_keywords:
                    clean_keyword = keyword.strip()
                    if not clean_keyword: continue
                    
                    pattern = r'\b' + re.escape(clean_keyword) + r'\b'
                    if re.search(pattern, career_name_lower) or re.search(pattern, career_industry_lower):
                        is_excluded = True
                        logging.info(f"Excluding '{career['name']}' due to keyword '{clean_keyword}'")
                        break 
            
            if not is_excluded:
                # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
                # Проверяем, есть ли score_vector и является ли он строкой
                if 'score_vector' in career and isinstance(career['score_vector'], str):
                    try:
                        # Преобразуем строку JSON в словарь Python
                        career['score_vector'] = json.loads(career['score_vector'])
                    except (json.JSONDecodeError, TypeError):
                        # Если данные некорректны, обнуляем их, чтобы не было ошибки на фронте
                        career['score_vector'] = None
                
                if 'embedding' in career: del career['embedding']
                final_careers.append(career)
            
        return jsonify(final_careers)
        
    except Exception as e:
        logging.error(f"Critical error in generate_cards: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)