import unittest
# from Src.DTO.domain_prototype import domain_prototype
# from Src.DTO.filter import filter
from Src.start_service import start_service
from Src.data_reposity import data_reposity
# from Src.Core.format_filter import format_filter

from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model

"""
Набор тестов для фильтрации
"""
class test_prototype(unittest.TestCase):
    
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()
    
    
    def test_create_warehouse(self):
        data = self.reposity.data[data_reposity.warehouse_key()]
        assert data[0].name == "Склад1"
        assert data[0].location == "ул. Баумана 222"
        
        
    def test_create_transaction(self):
        data = self.reposity.data[data_reposity.transaction_key()]
        assert len(data) == 5
        assert data[0].type.value == "Приход"