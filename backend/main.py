import os
import sys
import logging
import json
import sqlite3
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Импортируем нашу новую функцию
from to_pdf import generate_career_pdf
from chat import get_gemini_response

for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(key, None)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')
FONT_PATH = os.path.join(BASE_DIR, 'Roboto-Regular.ttf')

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
    except Exception:
        return None

def analyze_user_text_for_rules(text: str) -> dict:
    if not ANALYSIS_MODEL: return {"positive_summary": text, "exclusion_keywords": []}
    prompt = f"Ты — эксперт-профориентолог. Проанализируй текст и верни JSON {{\"positive_summary\": \"\", \"exclusion_keywords\": []}}. Текст: '{text}'"
    try:
        response = ANALYSIS_MODEL.generate_content(prompt)
        cleaned = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)
    except Exception:
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
        if not user_message: return jsonify({'error': 'No message'}), 400
        return jsonify({'response': get_gemini_response(user_message)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not genai: return jsonify({"error": "AI unavailable"}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '').strip()
        analysis = analyze_user_text_for_rules(additional_info) if additional_info else {"positive_summary": "", "exclusion_keywords": []}
        
        conn = get_db_connection()
        user_query = f"Интересы: {', '.join(selected_topics)}. Пожелания: {analysis.get('positive_summary')}"
        query_embedding = get_query_embedding(user_query)
        
        rows = conn.execute('SELECT * FROM careers WHERE embedding IS NOT NULL').fetchall()
        scored = []
        for row in rows:
            career = dict(row)
            sim = cosine_similarity(query_embedding, np.array(json.loads(career['embedding'])))
            scored.append((sim, career))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        final = []
        for _, c in scored:
            if len(final) >= 50: break
            if 'embedding' in c: del c['embedding']
            final.append(c)
        conn.close()
        return jsonify(final)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.get_json()
        saved_careers = data.get('saved_careers', [])
        if not saved_careers:
            return jsonify({'error': 'No careers'}), 400
        
        # Вызываем функцию из to_pdf.py
        pdf_buffer = generate_career_pdf(saved_careers, PROJECT_ROOT, FONT_PATH)
        
        return send_file(
            pdf_buffer, 
            as_attachment=True, 
            download_name='ProfoBuilder_Results.pdf', 
            mimetype='application/pdf'
        )
    except Exception as e:
        logging.error(f"PDF Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)