"""
substitute.py — применяет словарь замен к файлам в raw/ и пишет результат в knowledge_base/.

Ключевые принципы:
- Замены сортируются по длине ключа (от длинных к коротким), чтобы 'Darth Vader'
  сработал раньше, чем одиночное 'Vader' из другой группы.
- Используются границы слов (\b) в regex, чтобы не заменять подстроки
  внутри других слов ('force' не сработает внутри 'enforce').
- Регистр сохраняется: словарь содержит все нужные варианты капитализации.
- terms_map.json разбит на категории для читаемости — здесь мы его «разворачиваем»
  в плоский dict {original: replacement}.
"""

from __future__ import annotations
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent  # scripts/ → корень проекта
RAW_DIR = ROOT / "raw"
OUT_DIR = ROOT / "knowledge_base"
MAP_PATH = ROOT / "terms_map.json"


def load_flat_mapping(map_path: Path) -> dict[str, str]:
    """Плющит иерархический terms_map.json в плоский dict {orig: repl}."""
    data = json.loads(map_path.read_text(encoding="utf-8"))
    flat: dict[str, str] = {}
    for category, items in data.items():
        if category.startswith("_"):  # служебные ключи типа _meta пропускаем
            continue
        for original, replacement in items.items():
            flat[original] = replacement
    return flat


def build_regex_pattern(mapping: dict[str, str]) -> re.Pattern:
    """
    Собирает ОДНУ большую regex-паттерн с альтернативами, отсортированными
    по длине (длинные вперёд). Это гарантирует, что 'Darth Vader' попадётся
    раньше 'Vader', и мы не проделаем двойную замену.
    """
    # сортируем по длине убывания — длинные совпадения имеют приоритет
    keys_sorted = sorted(mapping.keys(), key=len, reverse=True)
    # экранируем спецсимволы и оборачиваем в группу
    escaped = [re.escape(k) for k in keys_sorted]
    # \b с обеих сторон: границы слов
    # но для фраз с дефисом (TIE-fighter) и пробелами \b работает корректно
    pattern = r"\b(" + "|".join(escaped) + r")\b"
    return re.compile(pattern)


def substitute(text: str, mapping: dict[str, str], pattern: re.Pattern) -> str:
    """Применяет замены по предсобранному regex."""
    def repl(match: re.Match) -> str:
        return mapping[match.group(0)]
    return pattern.sub(repl, text)


def main() -> None:
    mapping = load_flat_mapping(MAP_PATH)
    pattern = build_regex_pattern(mapping)

    OUT_DIR.mkdir(exist_ok=True)
    raw_files = sorted(RAW_DIR.glob("*.md"))
    if not raw_files:
        raise SystemExit(f"В {RAW_DIR} нет .md файлов. Сначала сгенерируй сырой контент.")

    stats = {"files": 0, "total_replacements": 0}
    for src in raw_files:
        text = src.read_text(encoding="utf-8")
        # считаем замены до применения, для статистики
        n = len(pattern.findall(text))
        new_text = substitute(text, mapping, pattern)

        # Имя выходного файла берём из H1 уже подставленного текста —
        # так имя файла тоже оказывается в вымышленном мире и бот не сможет
        # «угадать» исходный термин по имени файла.
        h1_match = re.search(r"^# (.+)$", new_text, re.MULTILINE)
        if h1_match:
            out_name = h1_match.group(1)
        else:
            # fallback: подставляем в исходный slug
            out_name = substitute(src.stem.replace("_", " "), mapping, pattern)
        out_slug = re.sub(r"[^a-zA-Z0-9]+", "_", out_name).strip("_").lower()
        out_path = OUT_DIR / f"{out_slug}.md"

        out_path.write_text(new_text, encoding="utf-8")
        stats["files"] += 1
        stats["total_replacements"] += n
        print(f"  {src.name:35s} → {out_path.name:35s} ({n} замен)")

    print(f"\nГотово: {stats['files']} файлов, {stats['total_replacements']} замен.")


if __name__ == "__main__":
    main()