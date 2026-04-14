from pathlib import Path

from numberlink.io.loader import load_text


def test_load_text_reads_file(tmp_path):
    """Проверяет, что load_text правильно читает содержимое файла."""
    file_path = tmp_path / "puzzle.txt"
    file_path.write_text("hex\nA . .\n. B .\nA . B\n", encoding="utf-8")

    result = load_text(file_path)

    assert result == "hex\nA . .\n. B .\nA . B\n"
