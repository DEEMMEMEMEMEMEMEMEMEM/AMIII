from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests
from datetime import datetime
import pytz

# === Настройки Telegram ===
BOT_TOKEN = "8151764416:AAE0F-wPCFZDViO7b5BQV-q7YjBHz0n8izA"  # Вставь настоящий токен сюда
CHAT_ID = "2110364647"  # Это твой Telegram chat ID (из /getUpdates)

# URL страницы стрима
URL = "https://www.donationalerts.com/r/amichkaplay"

# Часовой пояс Москвы
moscow_tz = pytz.timezone("Europe/Moscow")

def send_telegram_message(text):
    """Функция отправки сообщения в Telegram"""
    if not BOT_TOKEN or not CHAT_ID:
        print("Ошибка: не указан BOT_TOKEN или CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
        print("Сообщение отправлено в Telegram.")
    except requests.RequestException as e:
        print(f"Ошибка отправки в Telegram: {e}")

def check_stream():
    """Функция проверки стрима"""
    now = datetime.now(moscow_tz)
    current_hour = now.hour
    current_minute = now.minute

    if not (10 <= current_hour < 22 or (current_hour == 22 and current_minute <= 45)):
        print("Сейчас не время проверки. Ждем следующего окна...")
        return False  # Проверка не прошла, продолжать цикл

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Без графического интерфейса
    options.add_argument("--no-sandbox")  # Обход ограничений Railway
    options.add_argument("--disable-dev-shm-usage")  # Меньше памяти
    options.add_argument("--disable-gpu")  # Отключаем GPU

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Проверяю страницу {URL}...")
        driver.get(URL)
        time.sleep(5)

        try:
            element = driver.find_element(By.CLASS_NAME, "channel-status.online")
            print("Стример в эфире!")
            send_telegram_message("Ами начала подготовку к стриму!")
            return True  # Успешная проверка

        except:
            print("Ами пока что не готовится к стриму.")
            return False  # Стримера нет

    except Exception as e:
        print(f"Ошибка: {e}")
        return False  # Ошибка

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        successful_check = check_stream()
        if successful_check:
            print("Засыпаю на 6 часов после успешной проверки...")
            time.sleep(21600)  # Засыпаем на 6 часов
        else:
            print("Следующая проверка через 30 минут.")
            time.sleep(1800)  # Проверяем через 30 мину
