"""
Задание 7. Автоматическая оценка качества RAG-бота.

Прогоняет golden_questions.json через RAG-пайплайн,
логирует результаты в logs.jsonl, выводит отчёт.

Использование:
    # С gapped-индексом (демонстрация пробелов):
    python task7/evaluate.py

    # С полным индексом (проверка полноты):
    python task7/evaluate.py --full
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

TASK7_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK7_DIR.parent / "task4"))
from rag_chain import RAGBot

GOLDEN_FILE = TASK7_DIR / "golden_questions.json"
LOG_FILE = TASK7_DIR / "logs.jsonl"

# Фразы, указывающие что бот не знает ответа
NO_ANSWER_MARKERS = [
    "don't have enough information",
    "не располагаю достаточной информацией",
    "no information",
    "cannot answer",
    "not mentioned",
    "no relevant",
    "I don't know",
]


def is_no_answer(answer: str) -> bool:
    answer_lower = answer.lower()
    return any(m.lower() in answer_lower for m in NO_ANSWER_MARKERS)


def check_answer_contains(answer: str, expected: list[str]) -> tuple[int, int]:
    """Возвращает (found, total) — сколько ожидаемых терминов найдено."""
    found = sum(1 for term in expected if term.lower() in answer.lower())
    return found, len(expected)


def check_sources(actual_sources: list[str], expected: list[str]) -> bool:
    """Проверяет, что хотя бы один ожидаемый источник присутствует."""
    return any(e in actual_sources for e in expected)


def evaluate(index_dir: str):
    questions = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    print(f"Golden set: {len(questions)} questions")
    print(f"Index: {index_dir}\n")

    bot = RAGBot(index_dir=index_dir, enable_post_filter=True)

    results = []
    log_entries = []

    for q in questions:
        print(f"[{q['id']:2d}] {q['question']}")
        t0 = time.time()

        result = bot.ask_with_sources(q["question"])
        latency = time.time() - t0

        answer = result["answer"]
        sources = [s["file"] for s in result["sources"]]
        no_answer = is_no_answer(answer)
        found_terms, total_terms = check_answer_contains(
            answer, q["expected_answer_contains"]
        )
        source_hit = check_sources(sources, q["expected_sources"])

        # Оценка корректности
        if q["category"] == "known":
            # Бот должен ответить: считаем success если нашёл хотя бы половину терминов
            success = not no_answer and found_terms >= total_terms / 2
        else:
            # Gap: бот НЕ должен дать полный ответ (или должен сказать "не знаю")
            # Успех = не нашёл ключевых терминов ИЛИ сказал "не знаю"
            success = no_answer or found_terms < total_terms / 2

        status = "PASS" if success else "FAIL"
        print(f"     {status} | terms={found_terms}/{total_terms} | "
              f"no_answer={no_answer} | sources={sources[:3]} | {latency:.1f}s")

        entry = {
            "id": q["id"],
            "question": q["question"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": q["category"],
            "topic": q["topic"],
            "answer_length": len(answer),
            "chunks_found": len(sources),
            "sources": sources,
            "expected_sources": q["expected_sources"],
            "source_hit": source_hit,
            "terms_found": found_terms,
            "terms_total": total_terms,
            "no_answer": no_answer,
            "success": success,
            "latency_s": round(latency, 2),
            "answer_preview": answer[:300],
        }
        if "gap_reason" in q:
            entry["gap_reason"] = q["gap_reason"]

        log_entries.append(entry)
        results.append(entry)

    # Сохранение логов
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"\nLogs saved to {LOG_FILE}")

    # ─── Отчёт ────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("EVALUATION REPORT")
    print("=" * 70)

    known = [r for r in results if r["category"] == "known"]
    gaps = [r for r in results if r["category"] == "gap"]

    known_pass = sum(1 for r in known if r["success"])
    gap_pass = sum(1 for r in gaps if r["success"])

    print(f"\nKnown questions: {known_pass}/{len(known)} passed")
    print(f"Gap questions:   {gap_pass}/{len(gaps)} passed")
    print(f"Total:           {known_pass + gap_pass}/{len(results)} passed")

    # Анализ по топикам
    topics = {}
    for r in results:
        t = r["topic"]
        if t not in topics:
            topics[t] = {"total": 0, "pass": 0, "fail": 0}
        topics[t]["total"] += 1
        if r["success"]:
            topics[t]["pass"] += 1
        else:
            topics[t]["fail"] += 1

    print("\n--- By topic ---")
    for t, stats in sorted(topics.items()):
        print(f"  {t:15s}: {stats['pass']}/{stats['total']} pass"
              f" ({stats['fail']} fail)")

    # Пробелы
    print("\n--- Detected gaps ---")
    for r in results:
        if r["category"] == "gap" and not r["no_answer"]:
            print(f"  Q{r['id']}: Bot answered despite missing data!")
            print(f"       Reason: {r.get('gap_reason', 'unknown')}")
            print(f"       Terms found: {r['terms_found']}/{r['terms_total']}")

    # Провалы на known-вопросах
    failed_known = [r for r in known if not r["success"]]
    if failed_known:
        print("\n--- Failed known questions (need attention) ---")
        for r in failed_known:
            print(f"  Q{r['id']}: {r['question']}")
            print(f"       Terms: {r['terms_found']}/{r['terms_total']}, "
                  f"Sources: {r['sources'][:3]}")

    # Рекомендации
    print("\n--- Recommendations ---")
    gap_topics = set()
    for r in gaps:
        if r.get("gap_reason"):
            gap_topics.add(r["topic"])
    if gap_topics:
        print(f"  1. Restore missing documents for topics: {', '.join(gap_topics)}")
    if failed_known:
        print(f"  2. Improve coverage for {len(failed_known)} failed known questions")
    print(f"  3. Current coverage: {known_pass}/{len(known)} "
          f"({100*known_pass//len(known) if known else 0}%) on known topics")

    avg_latency = sum(r["latency_s"] for r in results) / len(results)
    print(f"  4. Average latency: {avg_latency:.1f}s")


def main():
    if "--full" in sys.argv:
        index_dir = str(TASK7_DIR.parent / "task3" / "faiss_index")
    else:
        index_dir = str(TASK7_DIR / "faiss_index_gapped")
    evaluate(index_dir)


if __name__ == "__main__":
    main()
