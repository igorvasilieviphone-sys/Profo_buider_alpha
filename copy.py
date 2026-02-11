import os
from pathlib import Path

def combine_files_to_single_txt():
    # Настройки путей
    source_dir = Path.cwd() 
    # Имя и путь итогового файла
    output_file_path = Path(r"D:\txt_project\PBuilderTXT\full_project_code_profobuilder.txt")
    
    # Настройки исключений
    ignored_dirs = {'.venv', 'venv', '__pycache__', '.git', '.idea', '.vscode'}
    ignored_extensions = {'.db', '.pyc', '.exe', '.bin', '.png', '.env', '.ttf', '.jpg'}
    ignored_files = {'generate_db.py', Path(__file__).name}

    # Создаем папку, если она не существует
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Сбор данных из: {source_dir}")
    print(f"Результат будет сохранен в: {output_file_path}")

    files_processed = 0

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(source_dir):
                current_path = Path(root)
                
                # Пропускаем игнорируемые папки
                if any(ignored in current_path.parts for ignored in ignored_dirs):
                    continue

                for file in files:
                    file_path = current_path / file
                    
                    # Проверка расширений
                    if file_path.suffix.lower() in ignored_extensions:
                        continue
                    
                    # Проверка конкретных имен файлов
                    if file in ignored_files:
                        continue

                    try:
                        # Читаем содержимое файла
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        
                        # Записываем заголовок (комментарий с названием файла)
                        outfile.write(f"{'='*50}\n")
                        outfile.write(f"// FILE: {file_path.relative_to(source_dir)}\n")
                        outfile.write(f"{'='*50}\n\n")
                        
                        # Записываем основной текст
                        outfile.write(content)
                        
                        # Добавляем 3 пустые строки в конце
                        outfile.write("\n\n\n")
                        
                        files_processed += 1
                        print(f"Добавлен: {file}")
                        
                    except Exception as e:
                        print(f"Ошибка при чтении файла {file}: {e}")

        print(f"\nГотово! Файлов объединено: {files_processed}")
        print(f"Файл создан по пути: {output_file_path}")

    except Exception as e:
        print(f"Критическая ошибка при записи итогового файла: {e}")

if __name__ == "__main__":
    combine_files_to_single_txt()