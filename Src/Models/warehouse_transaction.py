from Src.Core.base_models import base_model_name
from Src.Models.warehouse import warehouse_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model
from Src.Core.format_transaction import format_transaction
from Src.Core.validator import argument_exception, validator

import datetime


class warehouse_transaction(base_model_name):
    __warehouse: warehouse_model = None
    __nomenclature: nomenclature_model = None
    __range: range_model = None
    __quantity:int = 0
    __type = format_transaction
    __period: datetime.datetime = None
    
    
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
    Количество
    """
    @property
    def quantity(self) -> int:
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value:int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        self.__quantity = value
        
    
    """
    Тип транзакции
    """ 
    @property
    def type(self) -> format_transaction:
        return self.__type
    
    @type.setter
    def type(self, value: format_transaction):
        validator.validate(value, format_transaction)
        self.__type = value
        
        
    """
    Период
    """
    @property
    def period(self) -> datetime.datetime:
        return self.__period
    
    @period.setter
    def period(self, value:datetime.datetime):
        validator.validate(value, datetime.datetime)
        '''
        добавить проверку времени?
        
        if value <= :
            raise argument_exception("Некорректный аргумент!")
        '''
        self.__period = value
        
        
    """
    Фабричный метод
    """
    @staticmethod
    def create(warehouse: warehouse_model, nomenclature: nomenclature_model, range: range_model, 
               quantity: int, type: format_transaction = format_transaction, period = datetime.datetime.now()):
        
        validator.validate(quantity, int)
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(range, range_model)

        item = warehouse_transaction()
        item.warehouse = warehouse
        item.quantity = quantity
        item.nomenclature = nomenclature
        item.range = range
        item.type = type
        item.period = period
        return item
        