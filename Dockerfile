FROM python:3.11-slim

WORKDIR /app

# Системные зависимости для faiss-cpu и torch
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Зависимости Python (кэшируется отдельным слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код приложения
COPY task3/faiss_index/ ./task3/faiss_index/
COPY task4/ ./task4/

# Предзагрузка модели эмбеддингов при сборке (чтобы не качать при каждом запуске)
RUN python -c "from langchain_huggingface import HuggingFaceEmbeddings; \
    HuggingFaceEmbeddings(model_name='BAAI/bge-m3', model_kwargs={'device': 'cpu'})"

WORKDIR /app/task4

# По умолчанию запускаем Telegram-бота
# Для консольного: docker run -it rag-bot python console_bot.py
CMD ["python", "telegram_bot.py"]
