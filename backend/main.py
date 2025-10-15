# backend/main.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import json
import sqlite3
import random
import google.generativeai as genai
from dotenv import load_dotenv

from chat import gemini_client

logging.basicConfig(level=logging.INFO)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

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

def process_career_row(row):
    """Преобразует строку из БД в словарь и правильно парсит score_vector."""
    career_dict = dict(row)
    try:
        if career_dict.get('score_vector') and isinstance(career_dict['score_vector'], str):
            valid_json_string = career_dict['score_vector'].replace("'", "\"")
            career_dict['score_vector'] = json.loads(valid_json_string)
        elif not career_dict.get('score_vector'):
            career_dict['score_vector'] = {}
    except (json.JSONDecodeError, TypeError):
        logging.warning(f"Could not parse score_vector for career: {career_dict.get('name')}")
        career_dict['score_vector'] = {}
    return career_dict

@app.route('/')
def index():
    return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(PROJECT_ROOT, filename)

@app.route('/api/chat', methods=['POST'])
def handle_chat_message():
    try:
        from chat import get_gemini_response
        data = request.get_json()
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        ai_response_text = get_gemini_response(user_message)
        return jsonify({'response': ai_response_text})
    except Exception as e:
        logging.error(f"Internal server error in handle_chat_message: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

@app.route('/api/generate_cards', methods=['POST'])
def generate_cards():
    if not gemini_client:
        return jsonify({"error": "AI service is currently unavailable."}), 500

    try:
        data = request.get_json()
        selected_topics = data.get('selected_topics', [])
        additional_info = data.get('additional_info', '')
        if not selected_topics: return jsonify({'error': 'No topics provided'}), 400

        # ОБНОВЛЕННЫЙ ПРОМПТ: Запрашиваем название и описание
        prompt = (
            "Ты — эксперт по профориентации. Проанализируй интересы пользователя. "
            "Если текст который написал пользователь тебе непонятен или он не имеет смысла, не учитывай его при составлении ответов."
            "Твоя задача — сгенерировать список из 30 профессий. "
            "Для каждой профессии верни её точное название и краткое, интригующее описание в одно-два предложение (20-30 слов). "
            "Ответ должен быть СТРОГО валидным JSON-массивом объектов. "
            "Пример: [{\"name\": \"Веб-разработчик\", \"description\": \"Создает современные сайты и веб-приложения для бизнеса.\"}, {\"name\": \"UX/UI-дизайнер\", \"description\": \"Проектирует красивые и удобные интерфейсы для пользователей.\"}] "
            "Не добавляй ничего, кроме JSON-массива.\n\n"
            "Данные пользователя:\n"
            f"- Темы: {json.dumps(selected_topics, ensure_ascii=False)}\n"
            f"- Инфо: {additional_info}\n\n"
            "Особенно обращай внимание на - Инфо, в нем пользователь конкретно выражает свои мысли, попытайся скомбинировать ответы в - Темы и - Инфо чтобы найти медианную профессию в первую очередь, а затем уже выдавай наиболее подходящие в порядке убывания."
            "В первую очередь старайся выдать профессии удовлетворяющие введенному пользователем -Инфо(если оно есть) а затем уже пытайся найти медиану в - Темы и - Инфо"
            "Верни только JSON-массив из 30 объектов."
        )
        
        ai_recommendations = []
        try:
            logging.info("Generating career list with descriptions from AI...")
            model = genai.GenerativeModel('gemini-2.5-flash')
            generation_config = genai.GenerationConfig(response_mime_type="application/json")
            response = model.generate_content(contents=[prompt], generation_config=generation_config)
            ai_recommendations = json.loads(response.text)
            if not isinstance(ai_recommendations, list) or not all('name' in r and 'description' in r for r in ai_recommendations):
                raise ValueError("AI did not return the correct list of objects format.")
        except (json.JSONDecodeError, ValueError, Exception) as e:
            logging.error(f"Failed to get valid AI response: {e}. Using fallback.")
            conn = get_db_connection()
            if conn is None: return jsonify({'error': 'DB connection failed'}), 500
            fallback_careers = conn.execute('SELECT * FROM careers ORDER BY RANDOM() LIMIT 30').fetchall()
            conn.close()
            processed_careers = [process_career_row(row) for row in fallback_careers]
            for career in processed_careers:
                career['description'] = "Узнайте больше об этой востребованной и интересной специальности."
            return jsonify(processed_careers)

        if not ai_recommendations: return jsonify([])

        recommended_names = [rec['name'] for rec in ai_recommendations]
        descriptions_map = {rec['name']: rec['description'] for rec in ai_recommendations}
        
        conn = get_db_connection()
        if conn is None: return jsonify({'error': 'DB connection failed'}), 500
        
        placeholders = ','.join('?' for _ in recommended_names)
        query = f"SELECT * FROM careers WHERE name IN ({placeholders})"
        
        results_cursor = conn.execute(query, recommended_names).fetchall()
        careers_by_name = {row['name']: process_career_row(row) for row in results_cursor}
        
        final_careers = []
        for name in recommended_names:
            if name in careers_by_name:
                career_data = careers_by_name[name]
                # Добавляем описание от AI к данным из БД
                career_data['description'] = descriptions_map.get(name, "Краткое описание временно недоступно.")
                final_careers.append(career_data)

        # Добиваем до 30, если в нашей базе нашлось не все из списка AI
        if len(final_careers) < 30:
            needed = 30 - len(final_careers)
            existing_names = [c['name'] for c in final_careers] if final_careers else ['']
            placeholders_not_in = ','.join('?' for _ in existing_names)
            random_careers_cursor = conn.execute(
                f'SELECT * FROM careers WHERE name NOT IN ({placeholders_not_in}) ORDER BY RANDOM() LIMIT ?',
                existing_names + [needed]
            ).fetchall()
            for row in random_careers_cursor:
                career = process_career_row(row)
                career['description'] = "Узнайте больше об этой востребованной и интересной специальности."
                final_careers.append(career)

        conn.close()
        return jsonify(final_careers)
    except Exception as e:
        logging.error(f"Critical error in generate_cards: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
#    logging.info(f"Starting Flask server. Project root: {PROJECT_ROOT}")
#    app.run(debug=True, port=5000)