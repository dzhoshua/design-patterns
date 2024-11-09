from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity
from Src.Core.validator import operation_exception, validator
from Src.Models.group import group_model
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model
from Src.Services.observe_service import observe_service
from Src.DTO.domain_prototype import domain_prototype
from Src.DTO.filter import filter
from Src.Reports.report_factory import report_factory
from Src.settings_manager import settings_manager


"""
Сервис для работы с номенклатурой
"""
class nomenclature_service(abstract_logic):
    
    def __init__(self, reposity: data_reposity):
        observe_service.append(self)
        self.__reposity = reposity
        
        
    """
    Добавление номенклатуры
    """
    def put_nomenclature(self):
        pass
    
    
    """
    Изменение свойств номенклатуры
    """
    def patch_nomenclature(self):
        pass
    
    
    """
    Получение номенклатуры
    """
    def get_nomenclature(self, data: list[nomenclature_model], unique_code: str):
        
        item_filter = filter.create({"unique_code": unique_code})
        
        prototype = domain_prototype(data)
        prototype.create(item_filter)
        if not prototype.data:
            return []
        
        return prototype.data
    
    
    """
    Удаление номенклатуры
    """
    def delete_nomenclature(self):
        pass
    
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)
    
    
    def set_exception(self, ex: Exception):
        return super().set_exception(ex)