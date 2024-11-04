from Src.Core.abstract_processing import abstract_processing
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Models.warehouse_turnover import warehouse_turnover
from Src.Processors.calculations import calculations
from Src.Core.validator import validator, argument_exception
from datetime import datetime, timedelta
from Src.settings_manager import settings_manager
from Src.data_reposity import data_reposity

"""
Класс для расчёта оборотов
"""
class turnover_process(abstract_processing):
    
    
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self.block_period = datetime.strptime(self.manager.settings.block_period, "%Y-%m-%d")
    
    
    def processing(self, transactions: list[warehouse_transaction]):
        
        # reposity = data_reposity()
        # if reposity.blocked_turnover_key():
        #     blocked_turnovers = reposity.data[data_reposity.blocked_turnover_key()]
        # else:
        blocked_turnovers = {}
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
                else:
                    turnovers[key].turnover = quantity
        
        for key, turnover in blocked_turnovers.items():
            if key in turnovers:
                turnovers[key].turnover += turnover.turnover
            else:
                turnovers[key] = turnover

        turnovers = list(turnovers.values())

        return turnovers