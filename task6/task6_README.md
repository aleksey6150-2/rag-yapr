# Задание 6. Автоматическое ежедневное обновление базы знаний

## Источник данных

Локальная папка `task2/knowledge_base/` — симулирует корпоративное хранилище документов. В продакшене это может быть Confluence API, S3-бакет, Git-репозиторий или Google Drive.

Подхват новых файлов — по **SHA-256 хэшу**: скрипт сравнивает хэш каждого `.md` файла с сохранённым в `manifest.json`. Если хэш изменился или файла нет в манифесте — файл обрабатывается.

## Скрипт обновления

### `update_index.py`

```
Scan → Chunk → Embed → Update FAISS → Log
```

| Шаг | Что делает |
|---|---|
| Scan | Сравнивает SHA-256 файлов с manifest.json |
| Chunk | RecursiveCharacterTextSplitter (800 симв., 150 overlap) |
| Embed | BGE-M3 (1024 dim, CPU) |
| Update | `FAISS.add_documents()` инкрементально или `--force` для полной пересборки |
| Log | Файл + stdout: время, кол-во файлов, чанков, ошибки |

### Режимы запуска

```bash
python task6/update_index.py           # инкрементальное обновление
python task6/update_index.py --force   # полная переиндексация
```

### Обработка удалений

FAISS не поддерживает удаление векторов из HNSW-индекса. При обнаружении удалённых файлов скрипт логирует предупреждение и рекомендует `--force` для чистой пересборки.

## Периодический запуск (cron)

### Установка

```bash
chmod +x task6/setup_cron.sh
./task6/setup_cron.sh
```

Это добавит в crontab:
```
0 6 * * * cd /path/to/project && .venv/bin/python task6/update_index.py >> task6/logs/cron.log 2>&1
```

**Расписание:** каждый день в 06:00.

**При ошибке:** скрипт логирует traceback и выходит с кодом 1. Cron-лог сохраняется в `task6/logs/cron.log`. Для alerting в продакшене — добавить отправку в Slack/PagerDuty при ненулевом exit code.

### Удаление задачи

```bash
crontab -l | grep -v "update_index.py" | crontab -
```

## Логирование

Каждый запуск создаёт файл `task6/logs/update_YYYYMMDD_HHMMSS.log`.

Пример лога:
```
2026-04-16 14:50:45 [INFO] Index update started (force=False)
2026-04-16 14:50:45 [INFO] New/changed files: 1
2026-04-16 14:50:45 [INFO] Deleted files: 0
2026-04-16 14:50:45 [INFO]   shadow_nexus.md: 2 chunks
2026-04-16 14:50:45 [INFO] Added 2 chunks in 0.4s
2026-04-16 14:50:45 [INFO] Index updated at 2026-04-16 14:50:45
2026-04-16 14:50:45 [INFO]   Files processed: 1
2026-04-16 14:50:45 [INFO]   Total chunks in index: 74
2026-04-16 14:50:45 [INFO]   Total time: 7.5s
```

## Архитектурная диаграмма

Файл: [update_pipeline.puml](update_pipeline.puml)

Для визуализации: вставить содержимое в [plantuml.com/plantuml](http://www.plantuml.com/plantuml/uml/) или открыть в IDE с PlantUML-плагином.

## Тест: добавление нового документа

1. Добавил `shadow_nexus.md` в `knowledge_base/`
2. Запустил `python task6/update_index.py`
3. Результат: `New/changed files: 1`, `Added 2 chunks`, `Total chunks: 74`
4. Повторный запуск: `No changes detected. Index is up to date.`
5. Удалил файл, запустил `--force`: `Files deleted: 1`, `Total chunks: 72`

## Структура

```
task6/
├── task6_README.md           # этот файл
├── update_index.py           # скрипт обновления индекса
├── setup_cron.sh             # установка cron-задачи
├── update_pipeline.puml      # PlantUML диаграмма
├── manifest.json             # манифест обработанных файлов
└── logs/                     # логи обновлений
    ├── update_20260416_*.log
    └── cron.log              # лог cron-запусков
```
