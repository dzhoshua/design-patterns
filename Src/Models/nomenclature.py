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
        validator.validate(value,group_model )
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
        
        
    def to_dict(self):
        return {
            "name": self.name,
            "group": self.group.to_dict(),
            "range": self.range.to_dict()
        }
        
    """
    Переопределение получения аттрибутов и класса
    """
    @property
    def attribute_class(self) -> dict:
        return {
            "group": group_model,
            "range": range_model
            }
        
    """
    Фабричный метод
    """
    @staticmethod
    def create(name:str, range:range_model, group: group_model) -> 'nomenclature_model':
        validator.validate(name, str, 255)
        validator.validate(range, range_model)
        validator.validate(group, group_model)

        item = nomenclature_model()
        item.group = group
        item.range = range
        item.name = name
        return item