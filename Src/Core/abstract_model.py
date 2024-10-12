from abc import ABC, abstractmethod
import uuid


"""
Абстрактный класс для наследования моделей данных
"""
class abstract_model(ABC):
    __unique_code:str
    

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    

    """
    Класс у аттрибута
    """
    @property
    @abstractmethod
    def attribute_class(self) -> dict:
        pass
    
    
    """
    Абстрактный метод для преобразования в json
    """
    @abstractmethod
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            #"name": self.name,
        }
    

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
    

    def __str__(self) -> str:
        return self.unique_code
    
    
        