from Src.Core.validator import validator
from Src.Core.abstract_processing import abstract_processing
from Src.Managers.settings_manager import settings_manager
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.data_reposity import data_reposity
from datetime import datetime


"""
Расчет ОСВ
"""
class turnover_balanse_sheet(abstract_processing):
    
    def __init__(self, manager: settings_manager):
        super().__init__(manager)
    
    
    def processing(self, transactions: list[warehouse_transaction]):
        
        return super().processing(transactions)