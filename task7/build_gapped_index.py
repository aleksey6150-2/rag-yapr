"""
Строит FAISS-индекс из knowledge_base_gapped/ (без 3 ключевых сущностей).
"""

import time
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

KB_DIR = Path(__file__).resolve().parent / "knowledge_base_gapped"
INDEX_DIR = Path(__file__).resolve().parent / "faiss_index_gapped"
EMBEDDING_MODEL = "BAAI/bge-m3"


def main():
    loader = DirectoryLoader(
        str(KB_DIR), glob="*.md",
        loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents (3 removed: void_core, xarn_velgor, the_synth_flux)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=150,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        source_path = Path(chunk.metadata.get("source", ""))
        chunk.metadata["file_name"] = source_path.name
        chunk.metadata["title"] = source_path.stem.replace("_", " ").title()
        chunk.metadata["chunk_id"] = i
    print(f"Chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )

    t0 = time.time()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print(f"Index built in {time.time() - t0:.1f}s")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    print(f"Saved to {INDEX_DIR}")


if __name__ == "__main__":
    main()
