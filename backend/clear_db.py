import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'careers.db')

def clear_embeddings():
    if not os.path.exists(DB_PATH):
        print(f"Ошибка: База данных не найдена по пути {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем наличие колонки перед очисткой
        cursor.execute("PRAGMA table_info(careers)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'embedding' in columns:
            cursor.execute("UPDATE careers SET embedding = NULL")
            conn.commit()
            print("Успех: Колонка embedding очищена. Теперь можно запускать генерацию.")
        else:
            print("Колонка embedding еще не создана. Скрипт генерации создаст её автоматически.")
            
        conn.close()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    clear_embeddings()