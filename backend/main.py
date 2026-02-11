import os
import sys
import logging
import json
import sqlite3
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

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
    client = genai.Client(api_key=api_key)
    EMBEDDING_MODEL = 'models/gemini-embedding-001'
    ANALYSIS_MODEL = 'gemini-2.5-flash'
except Exception as e:
    logging.error(f"Setup error: {e}")
    client = None

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
    v1, v2 = np.array(v1), np.array(v2)
    norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0: return 0
    return np.dot(v1, v2) / (norm1 * norm2)

def get_query_embedding(text):
    if not client: return None
    try:
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text[:500],
            config={'task_type': 'RETRIEVAL_QUERY'}
        )
        return result.embeddings[0].values
    except Exception as e:
        logging.error(f"Embedding API Error: {e}")
        return None

def analyze_user_input(text, topics):
    if not client or not text: return {"keywords": [], "domains": [], "exclusion": []}
    prompt = f"Return JSON: keywords (list), domains (list), exclusion (list). Input: {text}, Topics: {topics}"
    try:
        response = client.models.generate_content(model=ANALYSIS_MODEL, contents=prompt)
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json)
    except:
        return {"keywords": [], "domains": [], "exclusion": []}

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
    if not client: return jsonify({"error": "AI unavailable"}), 503
    try:
        data = request.get_json()
        selected_topics = [topic.get('label', '') for topic in data.get('selected_topics', [])]
        additional_info = data.get('additional_info', '').strip()
        excluded_ids = data.get('excluded_ids', [])
        limit = data.get('limit', 20)
        
        analysis = analyze_user_input(additional_info, selected_topics)
        search_query = f"{additional_info} {', '.join(selected_topics)}"
        query_emb = get_query_embedding(search_query)
        
        if query_emb is None: return jsonify({"error": "AI failed"}), 500

        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM careers WHERE embedding IS NOT NULL').fetchall()
        
        scored_results = []
        keywords = [k.lower() for k in analysis.get('keywords', [])]

        for row in rows:
            career = dict(row)
            if career['id'] in excluded_ids: continue
            
            c_name = career['name'].lower()
            c_desc = (career.get('description') or "").lower()
            
            career_emb = json.loads(career['embedding'])
            sim = cosine_similarity(query_emb, career_emb)
            
            boost = 0
            for kw in keywords:
                if kw in c_name: boost += 0.2
                elif kw in c_desc: boost += 0.05
            
            scored_results.append((sim + boost, career))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        final_list = []
        for _, c in scored_results[:limit]:
            c_data = {k: v for k, v in c.items() if k != 'embedding'}
            if isinstance(c_data.get('score_vector'), str):
                try: c_data['score_vector'] = json.loads(c_data['score_vector'])
                except: c_data['score_vector'] = {}
            final_list.append(c_data)

        conn.close()
        return jsonify(final_list)
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': "Server Error"}), 500

@app.route('/api/export_pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.get_json()
        saved_careers = data.get('saved_careers', [])
        pdf_buffer = generate_career_pdf(saved_careers, PROJECT_ROOT, FONT_PATH)
        return send_file(pdf_buffer, as_attachment=True, download_name='Results.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)