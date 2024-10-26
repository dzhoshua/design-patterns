from enum import Enum

"""
Типы транзакции
"""
class format_transaction(Enum):
    INCOME = "Приход"
    EXPENDITURE = "Расход"