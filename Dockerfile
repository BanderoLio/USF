# Используйте официальный образ Python как базовый
FROM python:3.13-slim

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируйте файлы зависимостей в рабочую директорию
COPY requirements.txt ./

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код бота в рабочую директорию
COPY . .

# Запустите бота при старте контейнера
CMD [ "python", "./main.py" ]