from Src.Core.validator import validator
from Src.Core.abstract_processing import abstract_processing
from Src.Managers.settings_manager import settings_manager
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.data_reposity import data_reposity
from Src.Models.balanse_sheet import balanse_sheet
from datetime import datetime


"""
Расчет ОСВ
"""
class turnover_balanse_sheet(abstract_processing):
    
    def __init__(self, manager: settings_manager):
        self.manager = manager
        
    
    def processing(self, transactions: list[warehouse_transaction], 
                   date_start:datetime, date_end: datetime, warehouse_id: str):
        
        # balanse_sheet.create()
        pass