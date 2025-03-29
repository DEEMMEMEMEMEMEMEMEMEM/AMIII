# Используем Python 3.12
FROM python:3.12-slim

# Установка зависимостей для Chrome и Chromedriver
RUN apt update && apt install -y \
    wget unzip curl gnupg \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libxcomposite1 libxrandr2 libasound2 \
    libpangocairo-1.0-0 libgtk-3-0 libgbm-dev

# Добавляем ключи и репозиторий Google Chrome
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/keyrings/google-chrome.asc > /dev/null && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.asc] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Устанавливаем Chrome
RUN apt update && apt install -y google-chrome-stable

# Устанавливаем зависимости Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Запуск бота
CMD ["python", "bot.py"]