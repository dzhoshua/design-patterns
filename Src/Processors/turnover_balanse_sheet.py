from Src.Core.validator import validator
from Src.Core.abstract_processing import abstract_processing
from Src.Managers.settings_manager import settings_manager
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Models.balanse_sheet import balanse_sheet
from Src.DTO.domain_prototype import domain_prototype
from Src.DTO.filter import filter
from Src.Processors.turnover_process import turnover_process
from datetime import datetime


"""
Расчет ОСВ
"""
class turnover_balanse_sheet(abstract_processing):
    
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self._turnover_process = turnover_process(self.manager)
        
    
    def processing(self, transactions: list[warehouse_transaction], date_start: datetime, date_end: datetime, warehouse_name: str):
        
        start_transactions = []
        period_transactions = []
        
        for transaction in transactions:
            if transaction.warehouse.name == warehouse_name:
                if date_start <= transaction.period <= date_end:
                    period_transactions.append(transaction)
                        
                if transaction.period <= date_start:
                    start_transactions.append(transaction)
        
        remainder = self._turnover_process.processing(period_transactions)
        opening_remainder = self._turnover_process.processing(start_transactions)
        
        balanse_sheet_ = balanse_sheet.create(opening_remainder, remainder)
        return balanse_sheet_