from Src.Core.abstract_processing import abstract_processing
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Models.warehouse_turnover import warehouse_turnover
from Src.Processors.calculations import calculations
from Src.Core.validator import validator, argument_exception
from datetime import datetime, timedelta
from Src.settings_manager import settings_manager

"""
Класс для расчёта оборотов
"""
class turnover_process(abstract_processing):
    __start_period: datetime = None
    __end_period: datetime = None  
    
    
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self.block_period = self.manager.settings.block_period


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
        
        process = turnover_process()
        process.start_period = start_period
        process.end_period = end_period
        return process
    
    
    def processing(self, transactions: list[warehouse_transaction]):
        
        # получаем сохранённые обороты (сохранение ещё не сделано)
        turnovers = {}
        
        for transaction in transactions:
            
            if transaction.period > self.block_period:
                key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)
                quantity = 0
                condition = calculations(transaction.type)
                quantity = condition.transaction(quantity, transaction.quantity)
                
                if key not in turnovers:
                    turnovers[key] = warehouse_turnover.create(
                        warehouse=transaction.warehouse,
                        nomenclature=transaction.nomenclature,
                        range=transaction.range,
                        turnover = int(quantity)
                    )
                else:
                    turnovers[key].turnover = int(quantity)
            # if self.start_period <= transaction.period <= self.end_period:
            #     quantity = 0
            #     idx = -1
            #     for i, tur in enumerate(turnovers):
            #         if transaction.nomenclature == tur.nomenclature and transaction.warehouse == tur.warehouse:
            #             quantity = tur.turnover
            #             idx = i
            #             break
                
            #     condition = calculations(transaction.type)
            #     quantity = condition.transaction(quantity, transaction.quantity)
            #     if idx != -1:
            #         turnovers[idx].turnover = int(quantity)
            #     else:
            #         turnover = warehouse_turnover.create(transaction.warehouse, transaction.nomenclature, transaction.range, int(quantity))
            #         turnovers.append(turnover)

        return turnovers