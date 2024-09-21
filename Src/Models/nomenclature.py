from Src.Core.base_models import base_model_code
from Src.Models.group import group_model
from Src.Models.range import range_model
from Src.Core.validator import validator

"""
Модель номенклатуры
"""
class nomenclature_model(base_model_code):
    __name:str = ""
    __group: group_model = None
    __range: range_model = None

    """
    Наименование
    """
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value:str):
        validator.validate(value, str, 255)
        self.__name = value.strip()

    """
    Группа номенклатуры
    """
    @property
    def group(self) -> group_model:
        return self.__group

    @group.setter
    def group(self, value: group_model):
        validator.validate(value, group_model)
        self.__group = value    

    """
    Единица измерения
    """
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value
    