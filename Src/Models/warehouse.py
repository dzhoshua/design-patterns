from Src.Core.base_models import base_model_name
from Src.Core.validator import argument_exception, validator


class warehouse_model(base_model_name):
    __location: str = ""
    __name: str = ""
    
    
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
    Местонахождение (адресс)
    """
    @property
    def location(self) -> str:
        return self.__location
    
    @location.setter
    def location(self, value:str):
        validator.validate(value, str, 255)
        self.__location = value.strip()
        
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "name":self.name,
            "location": self.location
        }
        
        
    """
    Фабричный метод
    """
    @staticmethod
    def create(name: str, location: str):
        validator.validate(location, str)
        validator.validate(name, str)
        
        item = warehouse_model()
        item.location = location
        item.name = name
        return item
    
    
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "location": self.location,
            "name": self.name
        }