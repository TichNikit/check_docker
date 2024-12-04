
FROM python

# Устанавливаем рабочую директорию
WORKDIR /app

# Скопируем файл зависимостей first
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Если у вас есть миграции Alembic, то можно их применить
CMD ["alembic", "upgrade", "head"]

# Указываем команду для запуска приложения
# Например, с использованием uvicorn для FastAPI
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]

# На какой порт будем открывать приложение
EXPOSE 8000