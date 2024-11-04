import unittest
from Src.start_service import start_service
from Src.data_reposity import data_reposity

from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model

"""
Набор тестов для блокировки
"""
class test_blocking(unittest.TestCase):
    
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()
    
    
    
        
    
    