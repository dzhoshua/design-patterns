import unittest
from Src.settings_manager import settings_manager
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
    start = start_service(reposity)
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
        count = 100000
        transactions = self.create_transactions(count)
        assert len(transactions) == count
        
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
            
        
    def create_transactions(self, count: int):
        transactions = []
        warehouse = self.reposity.data[data_reposity.warehouse_key()][0] 
        nomenclatures = self.reposity.data[data_reposity.nomenclature_key()]
        
        count_iter = count // len(nomenclatures)
        for i in range(count_iter):
            for nomenclature in nomenclatures:
                range1 = nomenclature.range

                date = datetime.now() - timedelta( minutes=(count_iter-i) * len(nomenclatures) )
                if i * len(nomenclatures) > count // 1.2:
                    date = datetime.now() + timedelta( minutes=i * len(nomenclatures) )
                
                random_quantity = random.randint(10, 300)
                random_transaction_type = random.choice(list(format_transaction)) 

                transaction = warehouse_transaction.create(
                    warehouse,
                    nomenclature,
                    range1,
                    float(random_quantity),
                    random_transaction_type,
                    date 
                )
                transactions.append(transaction)
        return transactions