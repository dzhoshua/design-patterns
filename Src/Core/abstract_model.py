from abc import ABC, abstractmethod
import uuid


"""
Абстрактный класс для наследования моделей данных
"""
class abstract_model(ABC):
    __unique_code:str =  uuid.uuid4()

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__unique_code.hex
    

    """
    Вариант сравнения (по коду)
    """
    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is  None: return False
        if not isinstance(other_object, abstract_model): return False

        return self.__unique_code == other_object.unique_code
    
    """
    Перегрузка штатного варианта сравнения
    """
    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)
        

        
