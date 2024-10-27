from Src.Core.abstract_processing import abstract_processing
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Models.warehouse_turnover import warehouse_turnover
from Src.Warehouse.calculations import calculations
from Src.Core.format_transaction import format_transaction
from Src.Core.validator import validator, argument_exception
from datetime import datetime, timedelta

"""
Класс для расчёта оборотов
"""
class processing_factory(abstract_processing):
    __start_period: datetime = None
    __end_period: datetime = None  


    """
    Начало периода
    """
    @property
    def start_period(self) -> datetime:
        return self.__start_period
    
    @start_period.setter
    def start_period(self, start_period: datetime):
        validator.validate(start_period, datetime)
        self.__start_period = start_period


    """
    Конец периода
    """
    @property
    def end_period(self) -> datetime:
        return self.__end_period
    
    @end_period.setter
    def end_period(self, end_period: datetime):
        validator.validate(end_period, datetime)
        self.__end_period = end_period


    
    def create(data: dict = None):
        start_period = None
        end_period = None
        if data is not None:       
            start_period = data.get("start_period")
            end_period = data.get("end_period")
            validator.validate(start_period, str)
            validator.validate(end_period, str)
            
        if start_period is None:
            start_period = datetime(2024, 1, 1)
        if end_period is None:
            end_period = datetime.now() + timedelta(minutes=1)

        try:
            start_period = datetime.strptime(start_period, "%Y-%m-%dT%H:%M:%SZ")
            end_period = datetime.strptime(end_period, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            argument_exception(start_period)
            argument_exception(end_period)
        
        process = processing_factory()
        process.start_period = start_period
        process.end_period = end_period
        return process
    
    
    def processing(self, transactions: list[warehouse_transaction]):
        turnovers = [] 
        for transaction in transactions:
            if self.start_period <= transaction.period <= self.end_period:
                quantity = 0
                idx = -1
                for i, tur in enumerate(turnovers):
                    if transaction.nomenclature == tur.nomenclature and transaction.warehouse == tur.warehouse:
                        quantity = tur.turnover
                        idx = i
                        break
                
                condition = calculations(transaction.type)
                quantity = condition.transaction(quantity, transaction.quantity)
                if idx != -1:
                    turnovers[idx].turnover = int(quantity)
                else:
                    turnover = warehouse_turnover.create(transaction.warehouse, transaction.nomenclature, transaction.range, int(quantity))
                    turnovers.append(turnover)

        return turnovers