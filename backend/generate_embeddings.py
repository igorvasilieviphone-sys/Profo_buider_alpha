import sqlite3
from google import genai
import os
import json
import logging
import time
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if os.path.exists(DOTENV_PATH):
    load_dotenv(dotenv_path=DOTENV_PATH)
    logging.info(f"Loading environment variables from: {DOTENV_PATH}")
else:
    load_dotenv()

try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")
    client = genai.Client(api_key=api_key)
    logging.info("Gemini configured successfully.")
except Exception as e:
    logging.error(f"Failed to configure Gemini: {e}")
    client = None

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def add_embedding_column(conn):
    try:
        conn.execute('ALTER TABLE careers ADD COLUMN embedding BLOB')
        conn.commit()
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            logging.error(f"Failed to alter table: {e}")
            raise

def generate_embeddings():
    if not client:
        return

    conn = get_db_connection()
    if not conn:
        return

    add_embedding_column(conn)
    
    careers_to_process = conn.execute('SELECT id, name, industry FROM careers WHERE embedding IS NULL').fetchall()
    
    if not careers_to_process:
        conn.close()
        return

    model_id = 'gemini-embedding-001'

    for career in careers_to_process:
        try:
            text_to_embed = f"Профессия: {career['name']}. Отрасль: {career['industry']}"
            logging.info(f"Generating embedding for: '{career['name']}'...")
            
            result = client.models.embed_content(
                model=model_id,
                contents=text_to_embed,
                config={'task_type': 'RETRIEVAL_DOCUMENT'}
            )
            
            embedding_values = result.embeddings[0].values
            embedding_json = json.dumps(embedding_values)
            
            conn.execute('UPDATE careers SET embedding = ? WHERE id = ?', (embedding_json.encode('utf-8'), career['id']))
            conn.commit()
            logging.info(f"Successfully saved embedding for: {career['name']}")
            
            time.sleep(0.7)

        except Exception as e:
            if "429" in str(e):
                logging.warning("Rate limit reached. Sleeping for 20 seconds...")
                time.sleep(20)
            else:
                logging.error(f"Failed to process career ID {career['id']} ('{career['name']}'): {e}")

    conn.close()

if __name__ == '__main__':
    generate_embeddings()