import unittest
# from Src.DTO.domain_prototype import domain_prototype
# from Src.DTO.filter import filter
from Src.Services.start_service import start_service
from Src.data_reposity import data_reposity
# from Src.Core.format_filter import format_filter
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Processors.turnover_process import turnover_process
from Src.settings_manager import settings_manager


"""
Набор тестов для склада и оборотов
"""
class test_warehouse(unittest.TestCase):
    
    reposity = data_reposity()
    start = start_service(reposity)
    manager = settings_manager()
    _turnover_process = turnover_process(manager)
    start.create()
    
    warehouse = reposity.data[data_reposity.warehouse_key()][0] 
    nomenclature = reposity.data[data_reposity.nomenclature_key()][0] 
    range = reposity.data[data_reposity.range_key()][0]
    
    transactions = [
        warehouse_transaction.create(
                warehouse,
                nomenclature,
                range,
                100.0,
                format_transaction.INCOME  
            ),
        warehouse_transaction.create(
                warehouse,
                nomenclature,
                range,
                50.0,
                format_transaction.EXPENDITURE 
            ),
        warehouse_transaction.create(
                warehouse,
                nomenclature,
                range,
                25.0,
                format_transaction.EXPENDITURE 
            )
    ]
    
    
    def test_create_warehouse(self):
        data = self.reposity.data[data_reposity.warehouse_key()]
        assert data[0].name == "Склад1"
        assert data[0].location == "ул. Баумана 222"
        
        
    def test_create_transaction(self):
        data = self.reposity.data[data_reposity.transaction_key()]
        assert len(data) == 5
        assert data[0].type.value == "Приход"
        
    
    def test_calculations(self):
        turnover = self._turnover_process.processing(self.transactions)
        expected_turnover = 100.0 - 50.0 - 25.0
        actual_turnover = turnover[0].turnover
        
        assert expected_turnover == actual_turnover    