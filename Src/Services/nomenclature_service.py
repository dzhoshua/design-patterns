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
    def put_nomenclature(self, name: str, group_id: str, range_id: str ):
        nomenclature = self.__reposity.data[data_reposity.nomenclature_key()] or []
        group_ = self.__reposity.data[data_reposity.group_key()]
        range_ = self.__reposity.data[data_reposity.range_key()]
        if nomenclature:
            item_filter = filter.create({"name": name})
            prototype = domain_prototype(nomenclature)
            prototype.create(item_filter)
            if prototype.data:
                return f'Номенклатура с именем "{name}" уже существует!'
            
            item_filter = filter.create({"unique_code": group_id})
            prototype = domain_prototype(group_)
            prototype.create(item_filter)
            if not prototype.data:
                return f'Группа с кодом "{group_id}" не существует!'
            group_value = prototype.data[0]
            
            
            item_filter = filter.create({"unique_code": range_id})
            prototype = domain_prototype(range_)
            prototype.create(item_filter)
            if not prototype.data:
                return f'Единица измерения с кодом "{range_id}" не существует!'
            range_value = prototype.data[0]
        
        self.__reposity.data[data_reposity.nomenclature_key()].append(
            nomenclature_model.create(name, range_value, group_value))
        return "Номенклатура успешно создана!"
    
    
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