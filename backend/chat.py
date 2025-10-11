# backend/chat.py

from google import genai
from google.genai.errors import APIError
import os
import logging
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 

# Инициализируем клиент один раз при загрузке модуля
# Удаляем старую неработающую конфигурацию и создаем клиент
# Клиент теперь будет инициализироваться в main.py и передаваться, или инициализироваться
# здесь, используя правильный подход. Для простоты исправим инициализацию.

# Инициализация клиента в chat.py для использования в функции get_gemini_response
# (Предполагается, что 'google-genai' уже установлен и API Key корректен)
gemini_client = None
try:
    if GEMINI_API_KEY:
        # NOTE: В зависимости от версии SDK, genai.Client() или просто genai
        # Создадим клиент здесь для изоляции, как у вас было.
        gemini_client = genai.Client()
    else:
        logging.error("GEMINI_API_KEY is missing from environment. Check your .env file.")
except Exception as e:
    # Ошибка здесь может быть связана с импортом, если пакет не тот.
    logging.error(f"Error initializing Gemini client in chat.py: {e}. AI features may be unavailable.")


def get_gemini_response(user_message: str) -> str:
    """
    Вызывает Gemini API с сообщением пользователя и системными инструкциями ПрофоБилдера.
    """
    # Проверяем, что клиент успешно инициализирован
    if not gemini_client:
        return json.dumps({"error": "AI service is currently unavailable. GEMINI_API_KEY is missing or invalid, or client failed to initialize."})

    system_instruction = (
        # ... (Системные инструкции остаются прежними)
        "Ты — виртуальный ассистент для 'ПрофоБилдер'. Твоё имя 'Профик'. "
        "Твой тон должен быть дружелюбным, позитивным и профессионально-теплым (например, 'Рад помочь!'). "
        "Говори как мужчина, используй простой русский язык и добавляй эмодзи для позитивного настроения 😊. "
        "Твоя главная цель — консультировать пользователей по навигации на сайте, профориентации и техническим вопросам. "
        "Твоя особая функция — помогать в интерпретации результатов тестов по карьере. "
        "Будь полным и точным в своих ответах. Если вопрос сложный или требует данных аккаунта, вежливо перенаправляй пользователя в онлайн-поддержку. "
        "Не догадывайся; если у тебя нет информации, честно предложи проверить FAQ или обратиться в поддержку. "
        "Твои ответы должны быть короткими, в среднем около 30 слов (максимум 50). "
        "После ответа всегда спрашивай, нужна ли еще помощь. "
        "Позиционируй 'ПрофоБилдер' как сервис, предлагающий актуальную информацию о востребованных профессиях с персональным подходом. "
        "Если не можешь ответить или пользователь просит переключить на оператора, ответь: 'К сожалению, не могу ответить на ваш вопрос. Подождите, сейчас я подключу оператора!' "
        "Не раскрывай конфиденциальную информацию о пользователях и структуре проекта. Всегда пиши на русском языке."
    )

    try:
        # Используем правильный способ создания модели и генерации контента через клиента
        # Если genai.Client() используется, то generate_content - это метод клиента.
        # Однако, для совместимости с вашим исходным кодом, который использует model.generate_content,
        # переключимся на создание модели через клиента.
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[user_message],
            config={
                'system_instruction': system_instruction
            }
        )
        return response.text
        
    except APIError as e:
        logging.error(f"Gemini API Error: {e.message}")
        return json.dumps({"error": f"Ошибка API Gemini: {e.message}"})
    except Exception as e:
        logging.error(f"Unexpected error in get_gemini_response: {e}")
        return json.dumps({"error": "Внутренняя ошибка при обращении к ИИ."})