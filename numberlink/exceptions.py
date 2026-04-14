class NumberlinkError(Exception):
    """Базовый класс для всех исключений в Numberlink"""

    pass


class InputFormatError(NumberlinkError):
    """Исключение для ошибок формата входных данных"""

    pass


class InvalidPuzzleError(NumberlinkError):
    """Исключение для ошибок в логике головоломки (например, неправильное количество конечных точек)"""

    pass
