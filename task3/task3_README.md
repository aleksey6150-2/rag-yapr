# Задание 3. Создание векторного индекса базы знаний

## Эмбеддинг-модель

| Параметр | Значение |
|---|---|
| Модель | [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) |
| Размерность | 1024 |
| Тип | Локальная (sentence-transformers) |
| Мультиязычность | 100+ языков, включая финский/эстонский/шведский |

Выбор обоснован в Задании 1: BGE-M3 обходит OpenAI text-embedding-3-large на мультиязычных бенчмарках MTEB, работает локально (данные не покидают периметр), бесплатна.

## Чанкинг

| Параметр | Значение |
|---|---|
| Метод | `RecursiveCharacterTextSplitter` (LangChain) |
| Размер чанка | 800 символов (~150-200 слов) |
| Перекрытие | 150 символов |
| Разделители | `\n## `, `\n### `, `\n\n`, `\n`, `. `, ` ` |

Разделители приоритизируют границы заголовков markdown, чтобы чанки были логически связными. Перекрытие 150 символов гарантирует, что контекст на границе чанка не теряется.

## Результаты индексации

| Метрика | Значение |
|---|---|
| Документов загружено | 36 |
| Чанков в индексе | 72 |
| Мин. размер чанка | 75 символов |
| Макс. размер чанка | 789 символов |
| Средний размер чанка | 522 символа |
| Время индексации (FAISS) | 12.2 сек |
| Полное время (загрузка модели + индексация) | 101.7 сек |

## Метаданные чанков

Каждый чанк хранит:
- `source` — полный путь к исходному файлу
- `file_name` — имя файла (e.g. `kael_venarix.md`)
- `title` — заголовок, извлечённый из имени файла
- `chunk_id` — порядковый номер чанка

## Векторная БД

**FAISS** (faiss-cpu) — in-memory индекс, сохранённый на диск в `task3/faiss_index/`. Выбран для MVP-спринта как рекомендовано в Задании 1. На пилоте планируется миграция на ChromaDB.

## Примеры запросов

### Запрос 1: «Who is Kael Venarix?»
| # | Score | Источник | Чанк |
|---|---|---|---|
| 1 | 0.7233 | kael_venarix.md | Overview: сын Ankarin Venarix, рос на Seldaris... |
| 2 | 0.9570 | xarn_velgor.md | Family: жена Pyrenne, сын Kael, дочь Seryn... |
| 3 | 0.9616 | ozul.md | Training: Ozul тренировал Kael Venarix... |

### Запрос 2: «What is the Synth Flux?»
| # | Score | Источник | Чанк |
|---|---|---|---|
| 1 | 0.6612 | the_synth_flux.md | Overview: энергетическое поле, соединяющее всё живое... |
| 2 | 0.8268 | the_synth_flux.md | Abilities: телекинез, усиленные рефлексы... |
| 3 | 0.9269 | overlord_nocturn.md | Synth Flux Abilities: мастер Dorveth Current... |

### Запрос 3: «Tell me about the Void Core»
| # | Score | Источник | Чанк |
|---|---|---|---|
| 1 | 0.6652 | void_core.md | Overview: боевая станция размером с луну... |
| 2 | 0.8477 | void_core.md | First Void Core: уничтожена в Clash of Kareth... |
| 3 | 0.9382 | resonant_core.md | Кристалл для фокусировки суперлазера Void Core... |

> Score — L2-расстояние (FAISS `IndexFlatL2`). Меньше = ближе = релевантнее.

## Как воспроизвести

```bash
cd task3
pip install langchain langchain-community langchain-huggingface faiss-cpu sentence-transformers
python build_index.py       # создать индекс
python test_index.py        # тестовые запросы
python test_index.py "your custom query"  # свой запрос
```

## Структура

```
task3/
├── task3_README.md       # этот файл
├── build_index.py        # создание индекса
├── test_index.py         # тестирование запросов
└── faiss_index/          # сохранённый FAISS-индекс
    ├── index.faiss
    └── index.pkl
```
