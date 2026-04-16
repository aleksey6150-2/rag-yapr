"""
scrape.py — опциональный референсный скрипт. Показывает, как собирать
исходный контент из публичных вики (например, fandom.com) с помощью
requests + BeautifulSoup.

ВАЖНО:
- Этот скрипт НЕ запускается автоматически в нашем пайплайне. Для сдачи
  задания достаточно build_raw_content.py — он наполняет raw/ напрямую.
- Если решишь использовать настоящий скрейпинг, проверь robots.txt сайта,
  поставь разумный User-Agent и rate limit, уважай условия использования.
- Контент с fandom.com доступен под лицензией CC BY-SA, не забудь об
  атрибуции, если будешь публиковать что-то наружу.

Использование:
    pip install requests beautifulsoup4
    python scripts/scrape.py
"""

from __future__ import annotations
import re
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(
        "Нужны зависимости: pip install requests beautifulsoup4"
    )


RAW_DIR = Path(__file__).parent.parent / "raw"
USER_AGENT = "RAG-Practicum-Bot/0.1 (educational use)"
DELAY_SECONDS = 1.0  # пауза между запросами

# Список (slug, URL) — пары для скачивания
PAGES: list[tuple[str, str]] = [
    # Заполни своими URL'ами с выбранной вики.
    # Пример формата (URL'ы здесь — это шаблон, не реальные вызовы):
    # ("luke_skywalker", "https://example.fandom.com/wiki/Luke_Skywalker"),
]


def fetch_page(url: str) -> str:
    """Скачивает HTML страницы."""
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    return r.text


def extract_main_content(html: str) -> str:
    """
    Извлекает основной текст статьи. Эвристика для Fandom-вики:
    выкидываем навигацию, infobox-ы, ссылки на разделы, таблицы.
    Под другие сайты эвристика будет своя — проверяй структуру DOM.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Удаляем шумные элементы
    for selector in [
        "aside",  # infobox в Fandom
        "table",  # сравнительные таблицы
        ".reference",
        ".navbox",
        ".toc",
        "script",
        "style",
        "sup",  # сноски
    ]:
        for el in soup.select(selector):
            el.decompose()

    # Основной контейнер статьи
    main = soup.select_one(".mw-parser-output") or soup.select_one("#mw-content-text") or soup.body
    if main is None:
        return ""

    # Берём только заголовки и параграфы
    parts: list[str] = []
    for el in main.find_all(["h1", "h2", "h3", "p", "li"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name == "h1":
            parts.append(f"# {text}\n")
        elif el.name == "h2":
            parts.append(f"\n## {text}\n")
        elif el.name == "h3":
            parts.append(f"\n### {text}\n")
        elif el.name == "li":
            parts.append(f"- {text}")
        else:
            parts.append(text + "\n")

    text = "\n".join(parts)
    # схлопываем тройные переводы строк
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    if not PAGES:
        print(
            "PAGES пуст. Заполни список (slug, URL) парами в этом файле.\n"
            "Для сдачи задания достаточно запустить build_raw_content.py."
        )
        return

    RAW_DIR.mkdir(exist_ok=True)
    for slug, url in PAGES:
        print(f"  fetching {url} ...")
        try:
            html = fetch_page(url)
            content = extract_main_content(html)
            (RAW_DIR / f"{slug}.md").write_text(content, encoding="utf-8")
            print(f"    saved {slug}.md ({len(content)} chars)")
        except Exception as e:
            print(f"    ОШИБКА: {e}")
        time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    main()
