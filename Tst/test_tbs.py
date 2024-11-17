import unittest
from Src.Services.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Managers.settings_manager import settings_manager
from Src.Processors.turnover_process import turnover_process
from Src.Managers.reposity_manager import reposity_manager
from Src.Models.balanse_sheet import balanse_sheet
from Src.Processors.turnover_balanse_sheet import turnover_balanse_sheet
from Src.Services.observe_service import observe_service
from Src.Core.event_type import event_type
from datetime import datetime, timedelta
import os


class test_tbs(unittest.TestCase):
    reposity = data_reposity()
    manager = settings_manager()
    rep_manager = reposity_manager(reposity, manager)
    start = start_service(reposity, manager)
    _turnover_process = turnover_process(manager)
    tbs = turnover_balanse_sheet(manager)
    start.create()
    
    """
    Тест для рассчета ОСВ
    """
    def test_turnover_balanse_sheet(self):
        # Подготовка
        warehouse_name = self.reposity.data[data_reposity.warehouse_key()][0].name
        date_start = datetime.now() - timedelta(days=10)
        date_end = datetime.now()
        transactions = self.reposity.data[data_reposity.transaction_key()]

        # Дествие
        balanse_sheet_ = self.tbs.processing(transactions, date_start, date_end, warehouse_name)

        # Проверка
        assert balanse_sheet is not None
        assert isinstance(balanse_sheet_, balanse_sheet)
        
      
    """
    Тест для менеджера репозитория
    """  
    def test_save_and_restore_data(self):
        # Подготовка
        len_nomenclatures = len(self.reposity.data[data_reposity.nomenclature_key()])
        path = self.rep_manager.file_name
        # Действия 
        observe_service.raise_event(event_type.SAVE_DATA_REPOSITY)
        
        observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY)

        assert len_nomenclatures == len(self.reposity.data[data_reposity.nomenclature_key()])