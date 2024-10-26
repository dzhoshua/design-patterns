# 
# не доделано
# 


from Src.Core.abstract_processing import abstract_processing
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Models.warehouse_turnover import warehouse_turnover
from Src.Warehouse.calculations import calculations
from Src.Core.validator import validator, argument_exception
from datetime import datetime


class turnover_process(abstract_processing):
    __start_period: datetime = None
    __end_period: datetime = None
    __turnovers: list[warehouse_turnover] = []   


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


    """
    Обороты
    """
    @property
    def turnovers(self) -> list[warehouse_turnover]:
        return self.__turnovers
    
    @turnovers.setter
    def turnovers(self, turnovers: list[warehouse_turnover]):
        validator.validate(turnovers, list)
        self.__turnovers = turnovers



    @staticmethod
    def create(data: dict):
        start_period = data.get("start_period")
        end_period = data.get("end_period")

        if start_period is None:
            start_period = datetime(2024, 1, 1)
        if end_period is None:
            end_period = datetime.now()

        try:
            start_period = datetime.strptime(start_period, "%Y-%m-%dT%H:%M:%SZ")
            end_period = datetime.strptime(end_period, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            argument_exception(start_period)
            argument_exception(end_period)

        process = turnover_process()
        process.start_period = start_period
        process.end_period = end_period
        process.turnovers = []
        return process