from enum import Enum
from Src.Core.validator import validator


"""
Типы событий
"""
class event_type(Enum):
    DELETE_NOMENCLATURE = 1
    CHANGE_NOMENCLATURE = 2
    SAVE_DATA_REPOSITY = 3
    RESTORE_DATA_REPOSITY = 4