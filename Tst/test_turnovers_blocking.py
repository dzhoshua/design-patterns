import unittest
from Src.Managers.settings_manager import settings_manager
from Src.Services.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Processors.turnover_process import turnover_process
from Src.Processors.blocking_process import blocking_process
from datetime import datetime, timedelta
import random


"""
Набор тестов для блокировки
"""
class test_blocking(unittest.TestCase):
    
    reposity = data_reposity()
    reposity.data[data_reposity.blocked_turnover_key()] = {}
    manager = settings_manager()
    start = start_service(reposity, manager)
    start.create()
    
    
    _turnover_process = turnover_process(manager)
    _blocking_process = blocking_process(manager)
    
    transactions = reposity.data[data_reposity.transaction_key()]


    def test_blocking_calculations(self):
        original_block_period = self.manager.settings.block_period
        new_block_period = "2024-10-01"

        self.manager.settings.block_period = new_block_period

        # Рассчитаем оборот с новой датой блокировки
        turnover_results_with_new_block = self._turnover_process.processing(self.transactions)

        # Восстановим оригинальную дату блокировки
        self.manager.settings.block_period = original_block_period

        # Рассчитаем оборот с оригинальной датой блокировки
        turnover_results_with_original_block = self._turnover_process.processing(self.transactions)
        
        assert turnover_results_with_new_block == turnover_results_with_original_block
    
    
    """
    Нагрузочный тест
    """
    def test_load_blocking(self):
        transactions = self.transactions
        
        block_dates = [
            "2024-02-01",
            "2024-04-01",
            "2024-09-01"
        ]
        
        # считаем с блокировкой
        elapsed_time = []
        for block_date in block_dates:
            self.manager.settings.block_period = block_date
            
            start_time = datetime.now()
            self._blocking_process.processing(transactions)
            end_time = datetime.now()

            elapsed_time.append((end_time - start_time).total_seconds())
        
        
            
        with open('load_test_results.md', 'w', encoding="utf-8") as f:
            f.write("# Результаты нагрузочного теста\n\n")
            f.write("| Дата блокировки | Время расчета (с) |\n")
            f.write("|------------------|-------------------|\n")
            for i in range(len(block_dates)):
                f.write(f"| {block_dates[i]} | {elapsed_time[i]:.4f} |\n")
