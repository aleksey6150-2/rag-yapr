"""
Тестирование FAISS-индекса: загружает сохранённый индекс и выполняет поисковые запросы.

Использование:
    python task3/test_index.py
    python task3/test_index.py "свой запрос"
"""

import sys
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_DIR = Path(__file__).resolve().parent / "faiss_index"
EMBEDDING_MODEL = "BAAI/bge-m3"


def load_index():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.load_local(
        str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore


def search(vectorstore, query, k=3):
    print(f"\n>>> Запрос: {query}")
    results = vectorstore.similarity_search_with_score(query, k=k)
    for j, (doc, score) in enumerate(results, 1):
        preview = doc.page_content[:250].replace("\n", " ")
        print(f"  [{j}] score={score:.4f} | {doc.metadata['file_name']}"
              f" (chunk #{doc.metadata['chunk_id']})")
        print(f"      {preview}")
    print()
    return results


def main():
    print(f"Загрузка индекса из {INDEX_DIR}...")
    vectorstore = load_index()
    print(f"Индекс загружен. Чанков в индексе: {vectorstore.index.ntotal}")

    # Пользовательский запрос из аргументов
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search(vectorstore, query)
        return

    # Дефолтные тестовые запросы
    queries = [
        "Who is Kael Venarix and what is his story?",
        "What is the Synth Flux and how does it work?",
        "Tell me about the Void Core weapon",
        "What happened at the Battle of Kareth?",
        "Who are the members of the Free Coalition?",
    ]

    for q in queries:
        search(vectorstore, q)


if __name__ == "__main__":
    main()
