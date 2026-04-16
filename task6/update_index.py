"""
Задание 6. Автоматическое обновление векторного индекса.

Сканирует knowledge_base/ на новые и изменённые документы,
разбивает на чанки, генерирует эмбеддинги, обновляет FAISS-индекс.
Ведёт лог и хранит манифест обработанных файлов.

Использование:
    python task6/update_index.py              # обновить индекс
    python task6/update_index.py --force      # полная переиндексация
"""

import hashlib
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── Пути ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "task2" / "knowledge_base"
INDEX_DIR = ROOT / "task3" / "faiss_index"
MANIFEST_FILE = Path(__file__).resolve().parent / "manifest.json"
LOG_DIR = Path(__file__).resolve().parent / "logs"
EMBEDDING_MODEL = "BAAI/bge-m3"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ─── Логирование ─────────────────────────────────────────────────────────────
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def file_hash(path: Path) -> str:
    """SHA-256 хэш файла."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    """Загружает манифест: {filename: {hash, mtime, chunks_count}}."""
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict):
    MANIFEST_FILE.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def find_changes(manifest: dict, force: bool = False) -> tuple[list[Path], list[str]]:
    """Находит новые/изменённые файлы и удалённые файлы."""
    current_files = {f.name: f for f in KB_DIR.glob("*.md")}

    new_or_changed = []
    for name, path in current_files.items():
        if force:
            new_or_changed.append(path)
            continue
        h = file_hash(path)
        if name not in manifest or manifest[name]["hash"] != h:
            new_or_changed.append(path)

    deleted = [name for name in manifest if name not in current_files]

    return new_or_changed, deleted


def process_documents(files: list[Path]) -> list:
    """Загружает и разбивает документы на чанки."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )

    all_chunks = []
    for file_path in files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()
        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["file_name"] = file_path.name
            chunk.metadata["title"] = file_path.stem.replace("_", " ").title()
            chunk.metadata["indexed_at"] = datetime.now(timezone.utc).isoformat()

        all_chunks.extend(chunks)
        logger.info(f"  {file_path.name}: {len(chunks)} chunks")

    return all_chunks


def update_index(force: bool = False):
    """Главная функция обновления индекса."""
    t_start = time.time()
    logger.info("=" * 60)
    logger.info(f"Index update started (force={force})")
    logger.info(f"Knowledge base: {KB_DIR}")
    logger.info(f"Index dir: {INDEX_DIR}")

    manifest = load_manifest()
    changed_files, deleted_files = find_changes(manifest, force=force)

    if not changed_files and not deleted_files:
        logger.info("No changes detected. Index is up to date.")
        logger.info(f"Completed in {time.time() - t_start:.1f}s")
        return

    logger.info(f"New/changed files: {len(changed_files)}")
    logger.info(f"Deleted files: {len(deleted_files)}")

    # Загрузка модели эмбеддингов
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )

    if force or not INDEX_DIR.exists():
        # Полная переиндексация
        all_files = list(KB_DIR.glob("*.md"))
        logger.info(f"Full reindex: {len(all_files)} files")
        chunks = process_documents(all_files)

        # Назначаем chunk_id
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i

        t_index = time.time()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        logger.info(f"FAISS index built in {time.time() - t_index:.1f}s")

        # Обновляем манифест для всех файлов
        for f in all_files:
            manifest[f.name] = {
                "hash": file_hash(f),
                "mtime": f.stat().st_mtime,
                "chunks_count": sum(
                    1 for c in chunks if c.metadata["file_name"] == f.name
                ),
            }
    else:
        # Инкрементальное обновление
        logger.info("Loading existing index...")
        vectorstore = FAISS.load_local(
            str(INDEX_DIR), embeddings,
            allow_dangerous_deserialization=True,
        )

        if changed_files:
            logger.info(f"Processing {len(changed_files)} changed files...")
            new_chunks = process_documents(changed_files)

            # Назначаем chunk_id продолжая нумерацию
            start_id = vectorstore.index.ntotal
            for i, chunk in enumerate(new_chunks):
                chunk.metadata["chunk_id"] = start_id + i

            t_index = time.time()
            vectorstore.add_documents(new_chunks)
            logger.info(f"Added {len(new_chunks)} chunks in {time.time() - t_index:.1f}s")

            for f in changed_files:
                manifest[f.name] = {
                    "hash": file_hash(f),
                    "mtime": f.stat().st_mtime,
                    "chunks_count": sum(
                        1 for c in new_chunks if c.metadata["file_name"] == f.name
                    ),
                }

        if deleted_files:
            logger.info(f"Note: {len(deleted_files)} files deleted from source.")
            logger.info("  FAISS does not support true deletion. "
                        "Run with --force to rebuild clean index.")
            for name in deleted_files:
                del manifest[name]

    # Сохранение
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    save_manifest(manifest)

    total_chunks = vectorstore.index.ntotal
    elapsed = time.time() - t_start

    logger.info("-" * 60)
    logger.info(f"Index updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"  Files processed: {len(changed_files)}")
    logger.info(f"  Files deleted: {len(deleted_files)}")
    logger.info(f"  Total chunks in index: {total_chunks}")
    logger.info(f"  Total time: {elapsed:.1f}s")
    logger.info(f"  Log: {log_file}")
    logger.info("=" * 60)


def main():
    force = "--force" in sys.argv
    try:
        update_index(force=force)
    except Exception:
        logger.exception("Update failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
