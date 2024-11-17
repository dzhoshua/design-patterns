from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.Models.group import group_model
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.receipt import receipt_model
from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction


"""
Репозиторий данных
"""
class data_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance 


    """
    Набор данных
    """
    @property
    def data(self) :
        return self.__data


    """
    Ключ для хранения групп номенклатуры
    """
    @staticmethod
    def group_key() -> str:
        return "group"
    
    
    """
    Ключ для хранения номенклатуры
    """
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"
    
    
    """
    Ключ для хранения единиц измерения
    """
    @staticmethod
    def range_key() -> str:
        return "range"
    
    
    """
    Ключ для хранения рецептов
    """
    @staticmethod
    def receipt_key() -> str:
        return "receipt"
    
    
    """
    Ключ для хранения склада
    """
    @staticmethod
    def warehouse_key() -> str:
        return "warehouse"
    
    
    """
    Ключ для хранения транзакций
    """
    @staticmethod
    def transaction_key() -> str:
        return "transaction"
    
    
    """
    Ключ для хранения заблокированных оборотов
    """
    @staticmethod
    def blocked_turnover_key() -> str:
        return "blocked_turnover"
    
    
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(data_reposity) if
                    callable(getattr(data_reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(data_reposity, method)()
            result.append(key)

        return result
    
    
    @staticmethod
    def keys_and_models() -> dict:
        return {
            data_reposity.group_key(): group_model,
            data_reposity.nomenclature_key(): nomenclature_model,
            data_reposity.range_key(): range_model,
            data_reposity.receipt_key(): receipt_model,
            data_reposity.warehouse_key(): warehouse_model,
            data_reposity.transaction_key(): warehouse_transaction
        }
    
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)

    
    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    
       
    

    

