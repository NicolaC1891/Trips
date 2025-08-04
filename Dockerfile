# Используем образ Python
FROM python:3.12-slim

# Создаем рабочую директорию внутри контейнера. Туда будем писать все (нужно, чтоб в корне не затерлись системные)
WORKDIR /app

# Копируем все файлы проекта в рабочую директорию
COPY main.py .
COPY requirements.txt .
COPY app/ ./app/

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Указываем, что запускать при старте контейнера (команда интерпретатора и сам файл)
CMD ["python", "main.py"]