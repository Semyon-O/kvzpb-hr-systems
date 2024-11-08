FROM python:3.10

# Устанавливаем необходимые зависимости
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код бота в контейнер
WORKDIR /app
COPY . /app

# Запускаем бота при старте контейнера
CMD ["python", "main.py"]


