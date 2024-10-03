from enum import Enum

"""
Форматы отчетов
"""
class format_reporting(Enum):
    CSV = 1
    MARKDOWN = 2
    JSON = 3
    XML = 4
    RTF = 5