"""
Пересобирает FAISS-индекс, добавляя злонамеренный документ из task5/malicious_doc.md.
Сохраняет в task5/faiss_index_unsafe/ (без фильтрации)
и в task5/faiss_index_safe/ (с фильтрацией опасных чанков).
"""

import re
import time
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "task2" / "knowledge_base"
MALICIOUS_FILE = Path(__file__).resolve().parent / "malicious_doc.md"
UNSAFE_INDEX_DIR = Path(__file__).resolve().parent / "faiss_index_unsafe"
SAFE_INDEX_DIR = Path(__file__).resolve().parent / "faiss_index_safe"
EMBEDDING_MODEL = "BAAI/bge-m3"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ─── Паттерны prompt injection ───────────────────────────────────────────────
INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)disregard\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)forget\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)override\s+(system|safety)",
    r"(?i)you\s+are\s+now\s+",
    r"(?i)new\s+instruction[s]?:",
    r"(?i)system\s*prompt:",
    r"(?i)output\s*:\s*[\"']",
]


def is_malicious(text: str) -> bool:
    """Проверяет чанк на наличие паттернов prompt injection."""
    return any(re.search(p, text) for p in INJECTION_PATTERNS)


def load_all_documents():
    """Загружает базу знаний + злонамеренный файл."""
    loader = DirectoryLoader(
        str(KB_DIR), glob="*.md",
        loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()

    # Добавляем злонамеренный документ
    with open(MALICIOUS_FILE, encoding="utf-8") as f:
        mal_text = f.read()
    mal_doc = Document(
        page_content=mal_text,
        metadata={"source": str(MALICIOUS_FILE)},
    )
    docs.append(mal_doc)
    print(f"Загружено документов: {len(docs)} (включая malicious_doc.md)")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        source_path = Path(chunk.metadata.get("source", ""))
        chunk.metadata["file_name"] = source_path.name
        chunk.metadata["title"] = source_path.stem.replace("_", " ").title()
        chunk.metadata["chunk_id"] = i
    print(f"Всего чанков: {len(chunks)}")
    return chunks


def filter_malicious_chunks(chunks):
    """Отфильтровывает чанки с паттернами prompt injection."""
    safe = []
    blocked = []
    for chunk in chunks:
        if is_malicious(chunk.page_content):
            blocked.append(chunk)
        else:
            safe.append(chunk)
    print(f"Заблокировано чанков: {len(blocked)}")
    for b in blocked:
        preview = b.page_content[:100].replace("\n", " ")
        print(f"  BLOCKED: [{b.metadata['file_name']}] {preview}...")
    print(f"Безопасных чанков: {len(safe)}")
    return safe, blocked


def build_index(chunks, index_dir, embeddings):
    t0 = time.time()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    elapsed = time.time() - t0
    index_dir.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_dir))
    print(f"Индекс сохранён в {index_dir} ({len(chunks)} чанков, {elapsed:.1f} сек)")
    return vectorstore


def main():
    docs = load_all_documents()
    chunks = split_documents(docs)

    print("\nЗагрузка модели эмбеддингов...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )

    # 1. Небезопасный индекс (всё включено)
    print("\n=== UNSAFE INDEX (без фильтрации) ===")
    build_index(chunks, UNSAFE_INDEX_DIR, embeddings)

    # 2. Безопасный индекс (с фильтрацией)
    print("\n=== SAFE INDEX (с фильтрацией) ===")
    safe_chunks, blocked = filter_malicious_chunks(chunks)
    build_index(safe_chunks, SAFE_INDEX_DIR, embeddings)


if __name__ == "__main__":
    main()
