from __future__ import annotations

from pathlib import Path


def load_text(path: Path) -> str:
    """Загружает текст из файла и возвращает его содержимое"""
    return Path(path).read_text(encoding="utf-8")
