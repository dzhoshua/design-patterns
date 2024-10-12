from abc import ABC, abstractmethod
from Src.Core.validator import validator
import glob


"""
Абстрактный класс для обработки логики
"""
class abstract_logic(ABC):
    __error_text:str = ""

    """
    Описание ошибки
    """
    @property
    def error_text(self) -> str:
        return  self.__error_text.strip()
    
    
    @error_text.setter
    def error_text(self, message: str):
        validator.validate(message, str)
        self.__error_text = message.strip()

    """
    Флаг. Есть ошибка
    """
    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """
    Абстрактный метод для загрузки и обработки исключений
    """
    @abstractmethod
    def set_exception(self, ex: Exception):
        pass
    
    
    @staticmethod
    def file_search(file_name: str) -> str:
        validator.validate(file_name, str)

        path = f"./**/{file_name}"
        full_path = glob.glob(path, recursive=True)[0]
        
        validator.validatet(full_path, str)

        return full_path
       
