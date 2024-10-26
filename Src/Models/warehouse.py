from Src.Core.base_models import base_model_name
from Src.Core.validator import argument_exception, validator


class warehouse_model(base_model_name):
    __location: str = ""
    
    
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
        
        
    """
    Фабричный метод
    """
    @staticmethod
    def create(location: str):
        validator.validate(location, str)
        
        item = warehouse_model()
        item.location = location
        return item
    