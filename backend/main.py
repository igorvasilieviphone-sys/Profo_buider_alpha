import os
import sys

for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(key, None)

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
        raise ValueError("GEMINI_API_KEY missing")
    genai.configure(api_key=api_key, transport='rest')
    EMBEDDING_MODEL = 'gemini-embedding-001'
    ANALYSIS_MODEL = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    logging.error(f"Setup error: {e}")
    genai = None
    ANALYSIS_MODEL = None
    EMBEDDING_MODEL = None

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error:
        return None

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_query_embedding(text):
    if not genai or not EMBEDDING_MODEL: return None
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
            return jsonify({'error': 'No message'}), 400
        ai_response_text = get_gemini_response(user_message)
        return jsonify({'response': ai_response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not genai:
        return jsonify({"error": "AI unavailable"}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '').strip()

        if not selected_topics and not additional_info:
            return jsonify({'error': 'No input'}), 400

        analysis = analyze_user_text_for_rules(additional_info) if additional_info else {"positive_summary": "", "exclusion_keywords": []}
        positive_summary = analysis.get("positive_summary", "").strip()
        exclusion_keywords = analysis.get("exclusion_keywords", [])

        conn = get_db_connection()
        if not conn: return jsonify({'error': 'DB error'}), 500

        selected_topics_text = ", ".join(selected_topics)
        user_query = f"Интересы: {selected_topics_text}. Пожелания: {positive_summary}"
        query_embedding = get_query_embedding(user_query)
        
        if query_embedding is None:
            conn.close()
            return jsonify({"error": "AI query error"}), 500

        rows = conn.execute('SELECT * FROM careers WHERE embedding IS NOT NULL').fetchall()
        scored_careers = []
        for row in rows:
            career_data = dict(row)
            try:
                career_embedding = np.array(json.loads(career_data['embedding']))
                similarity = cosine_similarity(query_embedding, career_embedding)
                scored_careers.append((similarity, career_data))
            except:
                continue

        scored_careers.sort(key=lambda x: x[0], reverse=True)
        all_careers_raw = [c[1] for c in scored_careers]
        conn.close()

        final_careers = []
        for career in all_careers_raw:
            if len(final_careers) >= 50: break
            is_excluded = False
            career_text = (career['name'] + " " + career['industry']).lower()
            for kw in exclusion_keywords:
                if kw.lower() in career_text:
                    is_excluded = True
                    break
            if not is_excluded:
                if 'embedding' in career: del career['embedding']
                if 'score_vector' in career and isinstance(career['score_vector'], str):
                    try: career['score_vector'] = json.loads(career['score_vector'])
                    except: career['score_vector'] = None
                final_careers.append(career)

        return jsonify(final_careers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)