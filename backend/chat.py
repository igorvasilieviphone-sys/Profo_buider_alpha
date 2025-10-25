# backend/chat.py

import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

system_instruction = (
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

chat_model = None
if not API_KEY:
    logging.error("In chat.py: GEMINI_API_KEY is missing. Chat functionality will be disabled.")
else:
    try:
        genai.configure(api_key=API_KEY)
        chat_model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=system_instruction
        )
        logging.info("Chat model ('Профик') configured successfully in chat.py.")
    except Exception as e:
        logging.error(f"Failed to configure Gemini client in chat.py: {e}")

def get_gemini_response(user_message: str) -> str:
    if not chat_model:
        return "Извините, мой сервис чата сейчас недоступен из-за ошибки конфигурации. 🔧"

    try:
        response = chat_model.generate_content(user_message)
        return response.text
        
    except Exception as e:
        logging.error(f"Unexpected error in get_gemini_response: {e}")
        return "Ой, что-то пошло не так при обращении к моему AI. Попробуйте еще раз! 🤔"