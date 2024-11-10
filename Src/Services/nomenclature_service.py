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
            if self.get_filtered_data(nomenclature, name, "name"):
                return f'Номенклатура с именем "{name}" уже существует!'
            
            group_data = self.get_filtered_data(group_, group_id, "unique_code")
            if not group_data:
                return f'Группа с кодом "{group_id}" не существует!'
            group_value = group_data[0]
            
            range_data = self.get_filtered_data(range_, range_id, "unique_code")
            if not range_data:
                return f'Единица измерения с кодом "{range_id}" не существует!'
            range_value = range_data[0]
        
        self.__reposity.data[data_reposity.nomenclature_key()].append(
            nomenclature_model.create(name, range_value, group_value))
        return "Номенклатура успешно создана!"
    
    
    """
    Изменение свойств номенклатуры
    """
    def patch_nomenclature(self, unique_code: str, name: str, group_id: str, range_id: str ):
        nomenclature = self.__reposity.data[data_reposity.nomenclature_key()] or []
        group_ = self.__reposity.data[data_reposity.group_key()]
        range_ = self.__reposity.data[data_reposity.range_key()]
        
        if not nomenclature:
            return "База номенклатур пуста!"
        
        nom_data = self.get_filtered_data(nomenclature, unique_code, "unique_code")
        if not nom_data:
            return f'Номенклатура с кодом "{unique_code}" не существует!'
        nom_value = nom_data[0]
        
        group_data = self.get_filtered_data(group_, group_id, "unique_code")
        if not group_data:
            return f'Группа с кодом "{group_id}" не существует!'
        group_value = group_data[0]
        
        range_data = self.get_filtered_data(range_, range_id, "unique_code")
        if not range_data:
            return f'Единица измерения с кодом "{range_id}" не существует!'
        range_value = range_data[0]
        
        nom_value.name = name
        nom_value.range = range_value
        nom_value.group = group_value
        
        return "Номенклатура успешно обновлена!"
    
    
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
    
    def get_filtered_data(self,data: list, value:str, filter_name:str):
        item_filter = filter.create({filter_name: value})
        prototype = domain_prototype(data)
        prototype.create(item_filter)
        
        return prototype.data
    
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)
    
    
    def set_exception(self, ex: Exception):
        return super().set_exception(ex)