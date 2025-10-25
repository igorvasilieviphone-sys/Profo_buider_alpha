# backend/generate_embeddings.py

import sqlite3
import google.generativeai as genai
import os
import json
import logging
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
    logging.warning(f".env file not found at {DOTENV_PATH}. Make sure it exists in the project root.")
    load_dotenv()

try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
    genai.configure(api_key=api_key)
    logging.info("Gemini configured successfully.")
except Exception as e:
    logging.error(f"Failed to configure Gemini: {e}")
    genai = None

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
        logging.info("Column 'embedding' added to 'careers' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            logging.info("Column 'embedding' already exists. No changes made to the table structure.")
        else:
            logging.error(f"Failed to alter table: {e}")
            raise

def generate_embeddings():
    if not genai:
        logging.error("Gemini AI is not configured. Cannot generate embeddings.")
        return

    conn = get_db_connection()
    if not conn:
        return

    add_embedding_column(conn)
    
    careers_to_process = conn.execute('SELECT id, name, industry FROM careers WHERE embedding IS NULL').fetchall()
    
    if not careers_to_process:
        logging.info("No new careers to process. All embeddings seem to be up to date.")
        conn.close()
        return

    logging.info(f"Found {len(careers_to_process)} careers to process.")

    model = 'models/text-embedding-004'

    for career in careers_to_process:
        try:
            text_to_embed = f"Профессия: {career['name']}. Отрасль: {career['industry']}"
            
            logging.info(f"Generating embedding for: '{career['name']}'...")
            result = genai.embed_content(
                model=model,
                content=text_to_embed,
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            embedding_json = json.dumps(result['embedding'])
            conn.execute('UPDATE careers SET embedding = ? WHERE id = ?', (embedding_json.encode('utf-8'), career['id']))
            conn.commit()
            logging.info(f"Successfully saved embedding for: {career['name']}")

        except Exception as e:
            logging.error(f"Failed to process career ID {career['id']} ('{career['name']}'): {e}")

    conn.close()
    logging.info("Embedding generation process finished.")

if __name__ == '__main__':
    generate_embeddings()