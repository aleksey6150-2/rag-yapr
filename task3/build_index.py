"""
Задание 3. Создание векторного индекса базы знаний.

Загружает markdown-документы из task2/knowledge_base/,
разбивает на чанки, генерирует эмбеддинги через BGE-M3,
сохраняет FAISS-индекс в task3/faiss_index/.
"""

import time
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── Пути ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "task2" / "knowledge_base"
INDEX_DIR = Path(__file__).resolve().parent / "faiss_index"

# ─── Параметры ───────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "BAAI/bge-m3"
CHUNK_SIZE = 800        # символов (~150-200 слов, ~200-250 токенов)
CHUNK_OVERLAP = 150     # перекрытие для сохранения контекста на границах


def load_documents():
    """Загружает все .md файлы из knowledge_base/."""
    loader = DirectoryLoader(
        str(KB_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    print(f"Загружено документов: {len(docs)}")
    return docs


def split_documents(docs):
    """Разбивает документы на чанки с сохранением метаданных."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)

    # Обогащаем метаданные: имя файла, заголовок, id чанка
    for i, chunk in enumerate(chunks):
        source_path = Path(chunk.metadata.get("source", ""))
        chunk.metadata["file_name"] = source_path.name
        chunk.metadata["title"] = source_path.stem.replace("_", " ").title()
        chunk.metadata["chunk_id"] = i

    print(f"Получено чанков: {len(chunks)}")

    # Статистика по размерам
    lengths = [len(c.page_content) for c in chunks]
    print(f"  мин: {min(lengths)} симв., макс: {max(lengths)} симв., "
          f"среднее: {sum(lengths) // len(lengths)} симв.")
    return chunks


def create_embeddings():
    """Инициализирует модель эмбеддингов BGE-M3."""
    print(f"Загрузка модели {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )
    # Размерность
    test_vec = embeddings.embed_query("test")
    print(f"Размерность эмбеддингов: {len(test_vec)}")
    return embeddings


def build_and_save_index(chunks, embeddings):
    """Создаёт FAISS-индекс и сохраняет на диск."""
    print("Создание FAISS-индекса...")
    t0 = time.time()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    elapsed = time.time() - t0
    print(f"Индекс создан за {elapsed:.1f} сек.")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    print(f"Индекс сохранён в {INDEX_DIR}")

    return vectorstore, elapsed


def test_queries(vectorstore):
    """Проверяет индекс на нескольких примерах запросов."""
    queries = [
        "Who is Kael Venarix?",
        "What is the Synth Flux?",
        "Tell me about the Void Core",
    ]
    print("\n" + "=" * 70)
    print("ТЕСТОВЫЕ ЗАПРОСЫ")
    print("=" * 70)

    for query in queries:
        print(f"\n>>> Запрос: {query}")
        results = vectorstore.similarity_search_with_score(query, k=3)
        for j, (doc, score) in enumerate(results, 1):
            preview = doc.page_content[:200].replace("\n", " ")
            print(f"  [{j}] score={score:.4f} | {doc.metadata['file_name']}"
                  f" (chunk #{doc.metadata['chunk_id']})")
            print(f"      {preview}...")
        print()


def main():
    t_total = time.time()

    docs = load_documents()
    chunks = split_documents(docs)
    embeddings = create_embeddings()
    vectorstore, index_time = build_and_save_index(chunks, embeddings)
    test_queries(vectorstore)

    total = time.time() - t_total
    print("=" * 70)
    print("ИТОГО")
    print("=" * 70)
    print(f"  Документов:     {len(docs)}")
    print(f"  Чанков:         {len(chunks)}")
    print(f"  Модель:         {EMBEDDING_MODEL}")
    print(f"  Размерность:    1024")
    print(f"  Индексация:     {index_time:.1f} сек")
    print(f"  Полное время:   {total:.1f} сек")


if __name__ == "__main__":
    main()
