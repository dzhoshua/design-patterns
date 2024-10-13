import unittest
from Src.DTO.domain_prototype import domain_prototype
from Src.DTO.filter import filter
from Src.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Core.format_filter import format_filter

"""
Набор тестов для фильтрации
"""
class test_prototype(unittest.TestCase):
    
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()
    
    
    """
    EQUALS
    """
    def test_unique_code_equal(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        item_filter = filter()
        item_filter.unique_code = str(item.unique_code)
        item_filter.filter_name = format_filter.EQUALS
        prototype = domain_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0] == item
        
        
    def test__name_equals(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]

        item_filter = filter()
        item_filter.name = "Пшеничная мука"
        item_filter.filter_name = format_filter.EQUALS
        
        prototype = domain_prototype(data)
        
        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) == 1
        assert prototype.data[0].name == "Пшеничная мука"
        
        
    """
    LIKE
    """
    def test_name_like(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]

        item_filter = filter()
        item_filter.name = "а"
        item_filter.filter_name = format_filter.LIKE
        
        prototype = domain_prototype(data)
        
        # Действие
        prototype.create(data, item_filter)
        
        # Проверка
        assert len(prototype.data) == 4
        
        assert item_filter.name in prototype.data[0].name
            
            
    def test_unique_code_like(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]

        item_filter = filter()
        item_filter.unique_code = "0"
        
        item_filter.filter_unique_code = format_filter.LIKE
        prototype = domain_prototype(data)

        # Действие
        prototype.create(data, item_filter)
        print(prototype)
        
        # Проверка
        assert len(prototype.data) > 0
        assert item_filter.unique_code in prototype.data[0].unique_code
