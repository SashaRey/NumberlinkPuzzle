from pathlib import Path

def load_text_file(file_path: Path) -> str:
    """Загружает текст из файла и возвращает его содержимое"""
    with file_path.open('r', encoding='utf-8') as file:
        return file.read()