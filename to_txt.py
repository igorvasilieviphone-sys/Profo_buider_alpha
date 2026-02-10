import os
import shutil
from pathlib import Path

def create_txt_copies():
    source_dir = Path.cwd() 
    target_dir = Path(r"D:\txt_project\PBuilder")
    ignored_dirs = {'.venv', 'venv', '__pycache__', '.git', '.idea', '.vscode'}
    ignored_extensions = {'.db', '.pyc', '.exe', '.bin', '.png', '.env'}
    current_script = Path(__file__).name
    if target_dir.exists():
        print(f"Очистка целевой папки: {target_dir}")
        shutil.rmtree(target_dir)
    
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Начинаю сканирование: {source_dir}")

    count = 0
    for root, dirs, files in os.walk(source_dir):
        current_path = Path(root)
        if any(ignored in current_path.parts for ignored in ignored_dirs):
            continue

        for file in files:
            file_path = current_path / file
            if file == current_script:
                continue
            if file_path.suffix.lower() in ignored_extensions:
                continue
            target_file_path = target_dir / f"{file}.txt"

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                target_file_path.write_text(content, encoding='utf-8')
                count += 1
                print(f"Скопирован: {file}")
            except Exception as e:
                print(f"Ошибка при чтении {file}: {e}")

    print(f"\nГотово! Обработано файлов: {count}")
    print(f"Все копии находятся в: {target_dir}")

if __name__ == "__main__":
    create_txt_copies()