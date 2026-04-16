# Задание 7. Аналитика покрытия и качества базы знаний

## Методология

### 1. Искусственные пробелы

Из базы знаний (36 файлов) удалены 3 ключевых документа:

| Удалённый файл | Сущность | Тип |
|---|---|---|
| `void_core.md` | Void Core (боевая станция) | technology |
| `xarn_velgor.md` | Xarn Velgor (персонаж) | characters |
| `the_synth_flux.md` | Synth Flux (ключевая концепция) | concepts |

Gapped-индекс: 33 документа → 66 чанков (vs 72 в полном).

### 2. Golden set

13 вопросов ([golden_questions.json](golden_questions.json)):
- 8 вопросов на **известные темы** (бот должен ответить)
- 5 вопросов на **удалённые сущности** (бот должен сказать «не знаю» или дать неполный ответ)

Каждый вопрос содержит:
- Ожидаемые ключевые термины в ответе (`expected_answer_contains`)
- Ожидаемые источники (`expected_sources`)
- Категорию (`known` / `gap`)
- Тему (`characters`, `technology`, `factions`, `planets`, `concepts`)

### 3. Оценка корректности

- **Known:** PASS если бот нашёл ≥50% ожидаемых терминов и не сказал «не знаю»
- **Gap:** PASS если бот сказал «не знаю» ИЛИ нашёл <50% ожидаемых терминов

## Результаты

### Сводка

| Категория | PASS | FAIL | Accuracy |
|---|---|---|---|
| Known (8 вопросов) | 8 | 0 | **100%** |
| Gap (5 вопросов) | 1 | 4 | **20%** |
| **Всего** | **9** | **4** | **69%** |

### По топикам

| Топик | PASS/Total | Проблемы |
|---|---|---|
| characters | 3/5 | Gap-вопросы: бот находит инфо из смежных документов |
| concepts | 1/2 | Synth Flux упоминается в overlord_nocturn.md и др. |
| factions | 2/2 | Полное покрытие |
| planets | 1/1 | Полное покрытие |
| technology | 2/3 | Void Core упоминается в morvenn.md, free_coalition.md |

### Ключевое наблюдение: информационная утечка между документами

**4 из 5 gap-вопросов провалены** — бот собрал достаточно информации из *других* документов, где удалённые сущности упоминаются:

| Вопрос | Удалённый файл | Откуда бот взял информацию |
|---|---|---|
| Void Core | void_core.md | morvenn.md, free_coalition.md, kael_venarix.md |
| Xarn Velgor (кто такой) | xarn_velgor.md | ankarin_venarix.md, velran_tessik.md, kael_venarix.md |
| Synth Flux (что это) | the_synth_flux.md | overlord_nocturn.md, resonant_core.md |
| Xarn Velgor (как стал Dorveth) | xarn_velgor.md | ankarin_venarix.md, dorveth_pact.md |

**Вывод:** в хорошо связанной базе знаний удаление одного документа не создаёт полного пробела — информация «размазана» по смежным документам. Это и плюс (устойчивость к потере отдельных документов), и минус (сложнее обнаружить, что основной документ отсутствует).

### Единственный PASS среди gap-вопросов

**Q12:** «What are the two sides of the Synth Flux?» — бот правильно сказал «не знаю», потому что конкретные названия «Luminar» и «Dorveth» как двух сторон Flux описаны только в удалённом the_synth_flux.md.

## Рекомендации по улучшению базы знаний

1. **Восстановить недостающие документы.** Для production-базы три удалённых документа критичны — это ядро предметной области.

2. **Ввести «canonical document» тег.** Помечать основной документ для каждой сущности. Если canonical документ отсутствует — система должна предупреждать, даже если информация есть в смежных файлах.

3. **Добавить покрытие по событиям.** В golden set нет вопросов о конкретных событиях (Clash of Kareth, Dominion War). Стоит расширить golden set до 20-25 вопросов.

4. **Мониторинг «не знаю» ответов.** В production — агрегировать вопросы, на которые бот не ответил, и автоматически создавать тикеты на дополнение документации.

5. **Latency.** Среднее время ответа 22.5 сек (Ollama на CPU). Для production нужен GPU или облачный LLM — целевой latency <3 сек.

## Логирование

Каждый запрос записывается в `logs.jsonl` со следующими полями:

```json
{
  "id": 1,
  "question": "Who is Kael Venarix?",
  "timestamp": "2026-04-16T12:50:00Z",
  "category": "known",
  "topic": "characters",
  "answer_length": 450,
  "chunks_found": 4,
  "sources": ["kael_venarix.md", "ankarin_venarix.md"],
  "source_hit": true,
  "terms_found": 2,
  "terms_total": 2,
  "no_answer": false,
  "success": true,
  "latency_s": 34.1,
  "answer_preview": "1. Looking for..."
}
```

## Диаграмма

Sequence diagram: [evaluation_sequence.puml](evaluation_sequence.puml)

Показывает:
- Как обрабатывается запрос (User → UI → RAGBot → FAISS → Filter → LLM)
- Где может произойти сбой (пустой индекс, LLM timeout, injection)
- Как работает evaluate.py (golden set → RAGBot → logs → report)

## Как запустить

```bash
cd ~/workspace/yandex-arch/rag-yapr
source .venv/bin/activate

# Построить gapped-индекс
python task7/build_gapped_index.py

# Оценка на gapped-индексе (демонстрация пробелов)
python task7/evaluate.py

# Оценка на полном индексе (должно быть 13/13)
python task7/evaluate.py --full
```

## Структура

```
task7/
├── task7_README.md              # этот файл (отчёт)
├── golden_questions.json        # 13 вопросов с ожидаемыми ответами
├── evaluate.py                  # автоматическая оценка
├── build_gapped_index.py        # построение индекса с пробелами
├── evaluation_sequence.puml     # sequence diagram
├── knowledge_base_gapped/       # 33 файла (без 3 ключевых)
├── faiss_index_gapped/          # FAISS-индекс с пробелами
└── logs.jsonl                   # результаты оценки
```
