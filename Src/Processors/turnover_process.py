from Src.Core.abstract_processing import abstract_processing
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Models.warehouse_turnover import warehouse_turnover
from Src.Processors.calculations import calculations
from Src.Core.validator import validator, argument_exception
from datetime import datetime
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity
from Src.Core.logger_level import logger_level
from Src.Services.observe_service import observe_service


"""
Класс для расчёта оборотов
"""
class turnover_process(abstract_processing):
    
    
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self.block_period = datetime.strptime(self.manager.settings.block_period, "%Y-%m-%d")
    
    
    def processing(self, transactions: list[warehouse_transaction]):
        
        reposity = data_reposity()
        if reposity.blocked_turnover_key() not in reposity.data:
            reposity.data[data_reposity.blocked_turnover_key()] = {}
        blocked_turnovers = reposity.data[data_reposity.blocked_turnover_key()]
        turnovers = {}
        
        for transaction in transactions:
            
            if transaction.period > self.block_period:
                key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)
                quantity = 0.0
                condition = calculations(transaction.type)
                quantity = condition.transaction(transaction.quantity, quantity)
                
                if key not in turnovers:
                    turnovers[key] = warehouse_turnover.create(
                        warehouse=transaction.warehouse,
                        nomenclature=transaction.nomenclature,
                        range=transaction.range,
                        turnover = quantity
                    )
                    observe_service.raise_event(logger_level.INFO, "Создан новый складской оборот.")
                    observe_service.raise_event(logger_level.DEBUG, turnovers[key])
                else:
                    turnovers[key].turnover = quantity
        
        for key, turnover in blocked_turnovers.items():
            if key in turnovers:
                turnovers[key].turnover += turnover.turnover
            else:
                turnovers[key] = turnover

        turnovers = list(turnovers.values())

        return turnovers