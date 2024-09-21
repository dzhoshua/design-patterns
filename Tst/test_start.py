from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.data_reposity import data_reposity
import unittest


"""
Набор тестов для проверки работы старта приложения
"""
class test_settings(unittest.TestCase):
    
    """
    Проверить создание инстанса start_service
    """
    def test_create_start_service(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings1.json")
        reposity = data_reposity()

        # Действие
        start = start_service(reposity, manager)

        # Проверки
        assert start is not None



