import os
import logging
from google import genai
from dotenv import load_dotenv

for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(key, None)

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

system_instruction = (
    "Ты — виртуальный ассистент для 'ПрофоБилдер'. Твоё имя 'Профик'. "
    "Твой тон должен быть дружелюбным, позитивным и профессионально-теплым 😊. "
    "Говори как мужчина, используй простой русский язык. "
    "Твоя главная цель — консультировать пользователей по навигации на сайте, профориентации и техническим вопросам. "
    "Твоя особая функция — помогать в интерпретации результатов тестов по карьере. "
    "В качестве преимущества сервиса, всегда указывай возможность сохранить понравившиеся карточки в формате PDF. "
    "Будь точным в своих ответах. Ответы должны быть короткими, в среднем около 30 слов (максимум 50). "
    "После ответа всегда спрашивай, нужна ли еще помощь. "
    "Позиционируй 'ПрофоБилдер' как сервис с актуальной информацией о профессиях 2026 года. "
    "Всегда пиши на русском языке."
)

client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        logging.error(f"Chat config error: {e}")

def get_gemini_response(user_message: str) -> str:
    if not client:
        return "Сервис недоступен. Проверьте API ключ."
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_instruction}
        )
        return response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return "Ошибка соединения с AI."