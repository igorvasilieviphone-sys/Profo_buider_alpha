import os
import sys

print("--- Проверка переменных окружения ---")
for key, value in os.environ.items():
    if "45.155.68.129" in value or "PROXY" in key.upper():
        print(f"{key} = {value}")

print("\n--- Проверка путей поиска ---")
print(f"Текущий префикс (venv): {sys.prefix}")