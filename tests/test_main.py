import pytest

from numberlink import main as main_module
from numberlink.exceptions import NumberlinkError


class DummySolverWithSolution:
    def solve_all(self, puzzle, geometry):
        """Возвращает фиктивное решение для тестирования."""
        return [{"A": ["dummy-path"]}]


class DummySolverWithoutSolution:
    def solve_all(self, puzzle, geometry):
        """Возвращает пустой список, имитируя отсутствие решений."""
        return []


def test_main_prints_found_solution(monkeypatch, capsys):
    """Проверяет, что main правильно обрабатывает найденное решение."""
    monkeypatch.setattr(main_module, "load_text", lambda path: "text")
    monkeypatch.setattr(main_module, "parse_puzzle", lambda text: "puzzle")
    monkeypatch.setattr(main_module, "validate_puzzle", lambda puzzle: None)
    monkeypatch.setattr(main_module, "create_geometry", lambda puzzle: "geometry")
    monkeypatch.setattr(main_module, "BacktrackingSolver", lambda: DummySolverWithSolution())
    monkeypatch.setattr(main_module, "render_solution", lambda puzzle, solution: print("RENDERED"))

    monkeypatch.setattr(
        main_module, "build_parser",
        lambda: type(
            "DummyParser",
            (),
            {"parse_args": lambda self: type("Args", (), {"path": "puzzle.txt", "debug": False})()}
        )()
    )

    main_module.main()

    captured = capsys.readouterr()
    assert "Найдено 1 решение" in captured.out
    assert "Решение 1:" in captured.out
    assert "RENDERED" in captured.out


def test_main_prints_no_solution(monkeypatch, capsys):
    """Проверяет, что main правильно обрабатывает отсутствие решений."""
    monkeypatch.setattr(main_module, "load_text", lambda path: "text")
    monkeypatch.setattr(main_module, "parse_puzzle", lambda text: "puzzle")
    monkeypatch.setattr(main_module, "validate_puzzle", lambda puzzle: None)
    monkeypatch.setattr(main_module, "create_geometry", lambda puzzle: "geometry")
    monkeypatch.setattr(main_module, "BacktrackingSolver", lambda: DummySolverWithoutSolution())
    monkeypatch.setattr(main_module, "render_solution", lambda puzzle, solution: None)

    monkeypatch.setattr(
        main_module, "build_parser",
        lambda: type(
            "DummyParser",
            (),
            {"parse_args": lambda self: type("Args", (), {"path": "puzzle.txt", "debug": False})()}
        )()
    )

    main_module.main()

    captured = capsys.readouterr()
    assert "Решений не найдено" in captured.out


def test_main_handles_file_not_found(monkeypatch, capsys):
    """Проверяет, что main правильно обрабатывает ситуацию, когда файл не найден."""
    def raise_file_not_found(path):
        raise FileNotFoundError

    monkeypatch.setattr(main_module, "load_text", raise_file_not_found)

    monkeypatch.setattr(
        main_module, "build_parser",
        lambda: type(
            "DummyParser",
            (),
            {"parse_args": lambda self: type("Args", (), {"path": "missing.txt", "debug": False})()}
        )()
    )

    main_module.main()

    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_main_handles_numberlink_error(monkeypatch, capsys):
    """Проверяет, что main правильно обрабатывает NumberlinkError."""
    monkeypatch.setattr(main_module, "load_text", lambda path: "text")

    def raise_numberlink_error(text):
        raise NumberlinkError("bad puzzle")

    monkeypatch.setattr(main_module, "parse_puzzle", raise_numberlink_error)

    monkeypatch.setattr(
        main_module, "build_parser",
        lambda: type(
            "DummyParser",
            (),
            {"parse_args": lambda self: type("Args", (), {"path": "puzzle.txt", "debug": False})()}
        )()
    )

    main_module.main()

    captured = capsys.readouterr()
    assert "Ошибка: bad puzzle" in captured.out