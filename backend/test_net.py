import requests
try:
    response = requests.get('https://api.ipify.org?format=json', timeout=10)
    print(f"Python видит этот IP: {response.json()['ip']}")
    google_check = requests.get('https://www.google.com', timeout=10)
    print("Google доступен!")
except Exception as e:
    print(f"Ошибка сети: {e}")