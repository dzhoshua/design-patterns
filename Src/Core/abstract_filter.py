from abc import ABC, abstractmethod
from Src.Core.validator import validator


class abstract_filter(ABC):
    __data = []
    
    def __init__(self, source: list) -> None:
        super().__init__()
        validator.validate(source, list)
        self.__data = source
        
        
    @property
    def data(self) -> list:
        return self.__data
    
    
    @data.setter
    def data(self, data: list):
        validator.validate(data, list)
        self.__data = data
        
        
    @abstractmethod
    def create(self, data: list, filter):
        pass
    
        