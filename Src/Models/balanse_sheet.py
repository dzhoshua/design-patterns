from Src.Core.base_models import base_model_code
from Src.Models.warehouse import warehouse_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model
from Src.Core.validator import argument_exception, validator


class balanse_sheet(base_model_code):
    __warehouse: warehouse_model
    
    
    """
    Склад
    """
    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse
    

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        validator.validate(value, warehouse_model)
        self.__warehouse = value
      
        
    """
    Номенклатура
    """
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value
        
    
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
        
    
    """
    Оборот
    """
    @property
    def turnover(self) -> int:
        return self.__turnover
    
    @turnover.setter
    def turnover(self, value:float):
        validator.validate(value, float)
        if value < 0.0:
            raise argument_exception("Некорректный аргумент!")
        self.__turnover = value
        
        
    """
    Фабричный метод
    """
    # @staticmethod
    # def create(warehouse: warehouse_model, start_turnover: float):
        
    #     # validator.validate(turnover, float)
    #     # validator.validate(nomenclature, nomenclature_model)
    #     # validator.validate(warehouse, warehouse_model)
    #     # validator.validate(range, range_model)

    #     # item = balanse_sheet()
    #     # item.warehouse = warehouse
    #     # item.nomenclature = nomenclature
    #     # item.range = range
    #     # item.turnover = turnover
    #     return item
    
    
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "warehouse": self.warehouse.to_dict(),
            "nomenclature": self.nomenclature.to_dict(),
            "range": self.range.to_dict(),
            "turnover": self.turnover
        }