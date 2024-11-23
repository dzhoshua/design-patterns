from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity
from Src.Core.validator import operation_exception, validator
from Src.Models.nomenclature import nomenclature_model
from Src.Services.observe_service import observe_service
from Src.DTO.domain_prototype import domain_prototype
from Src.DTO.filter import filter
from Src.Core.logger_level import logger_level


"""
Сервис для работы с номенклатурой
"""
class nomenclature_service(abstract_logic):
    
    def __init__(self, reposity: data_reposity):
        observe_service.append(self)
        self.__reposity = reposity
    
    
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
    Добавление номенклатуры
    """
    def put_nomenclature(self, name: str, group_id: str, range_id: str ):
        nomenclature = self.__reposity.data[data_reposity.nomenclature_key()] or []
        group_ = self.__reposity.data[data_reposity.group_key()]
        range_ = self.__reposity.data[data_reposity.range_key()]
        
        if nomenclature:
            if self.get_filtered_data(nomenclature, name, "name"):
                message = f'Номенклатура с именем "{name}" уже существует!'
                observe_service.raise_event(logger_level.INFO, message)
                return message
            
            group_data = self.get_filtered_data(group_, group_id, "unique_code")
            if not group_data:
                message = f'Группа с кодом "{group_id}" не существует!'
                observe_service.raise_event(logger_level.ERROR, message)
                return message
            group_value = group_data[0]
            
            range_data = self.get_filtered_data(range_, range_id, "unique_code")
            if not range_data:
                message = f'Единица измерения с кодом "{range_id}" не существует!'
                observe_service.raise_event(logger_level.ERROR, message)
                return message
            range_value = range_data[0]
        
        self.__reposity.data[data_reposity.nomenclature_key()].append(
            nomenclature_model.create(name, range_value, group_value))
        
        message = f"Номенклатура '{name}' успешно создана!"
        observe_service.raise_event(logger_level.INFO, message)
        return message
    
    
    """
    Изменение свойств номенклатуры
    """
    def patch_nomenclature(self, data: dict):
        unique_code = data.get("unique_code") 
        name = data.get("name") 
        group_id = data.get("group_id")
        range_id = data.get("range_id")
        
        nomenclature = self.__reposity.data[data_reposity.nomenclature_key()] or []
        group_ = self.__reposity.data[data_reposity.group_key()]
        range_ = self.__reposity.data[data_reposity.range_key()]
        
        if not nomenclature:
            message = "База номенклатур пуста!"
            observe_service.raise_event(logger_level.INFO, message)
            return message
        
        nom_data = self.get_filtered_data(nomenclature, unique_code, "unique_code")
        if not nom_data:
            message = f'Номенклатура с кодом "{unique_code}" не существует!'
            observe_service.raise_event(logger_level.ERROR, message)
            return message
        nom_value = nom_data[0]
        
        group_data = self.get_filtered_data(group_, group_id, "unique_code")
        if not group_data:
            message = f'Группа с кодом "{group_id}" не существует!'
            observe_service.raise_event(logger_level.ERROR, message)
            return message
        group_value = group_data[0]
        
        range_data = self.get_filtered_data(range_, range_id, "unique_code")
        if not range_data:
            message = f'Единица измерения с кодом "{range_id}" не существует!'
            observe_service.raise_event(logger_level.ERROR, message)
            return message
        range_value = range_data[0]
        
        # Изменение номенклатуры в data_reposity
        nom_value.name = name
        nom_value.range = range_value
        nom_value.group = group_value
        
        # Изменение номенклатуры в рецептах
        recipes = self.__reposity.data[data_reposity.receipt_key()]
        self.find_nomenclature_in_recipes(recipes, unique_code, nom_value, True)
        observe_service.raise_event(logger_level.DEBUG, f"Номенклатура с кодом '{unique_code} была обновлена в рецептах.")
        
        # Изменение номенклатуры в сохранённых оборотах
        transactions = self.__reposity.data[data_reposity.transaction_key()]
        self.find_nomenclature_in_transactions(transactions, unique_code, nom_value, True)
        observe_service.raise_event(logger_level.DEBUG, f"Номенклатура с кодом '{unique_code} была обновлена в сохранённых оборотах.")
        
        message = f"Номенклатура с кодом '{unique_code}' успешно обновлена!"
        observe_service.raise_event(logger_level.INFO, message)
        return message
    
    
    """
    Удаление номенклатуры
    """
    def delete_nomenclature(self, unique_code: str):
        nomenclature = self.__reposity.data[data_reposity.nomenclature_key()]
        if not nomenclature:
            message = "База номенклатур пуста!"
            observe_service.raise_event(logger_level.INFO, message)
            return message
        
        nom_data = self.get_filtered_data(nomenclature, unique_code, "unique_code")
        if not nom_data:
            message = f'Номенклатура с кодом "{unique_code}" не существует!'
            observe_service.raise_event(logger_level.ERROR, message)
            return message
        
        # Проверка использования в рецептах и в сохраненных оборотах
        recipes = self.__reposity.data[data_reposity.receipt_key()]
        transactions = self.__reposity.data[data_reposity.transaction_key()]
        nom_in_recipes = self.find_nomenclature_in_recipes(recipes, unique_code)
        nom_in_transactions = self.find_nomenclature_in_transactions(transactions, unique_code)
    
        if nom_in_recipes or nom_in_transactions:
            message = f'Номенклатура с кодом "{unique_code}" используется в рецептах или в сохраненных данных и не может быть удалена!'
            observe_service.raise_event(logger_level.ERROR, message)
            return message
        
        # Удаление
        self.__reposity.data[data_reposity.nomenclature_key()] = [
            n for n in self.__reposity.data[data_reposity.nomenclature_key()] if n.unique_code != unique_code
        ]
        message = f"Номенклатура с кодом '{unique_code}' успешно удалена!"
        observe_service.raise_event(logger_level.INFO, message)
        return message
        
    
    def get_filtered_data(self,data: list, value:str, filter_name:str):
        item_filter = filter.create({filter_name: value})
        prototype = domain_prototype(data)
        prototype.create(item_filter)
        
        return prototype.data
    
    
    def find_nomenclature_in_recipes(self, data: list, unique_code: str, nom_data = None, is_patch = False):
        for item in data:
            for ingredient in item.ingredients:
                if ingredient.nomenclature.unique_code == unique_code:
                    if is_patch:
                        self.set_nom_values(ingredient, nom_data)
                    else:
                        return True
        return False
    
    
    def find_nomenclature_in_transactions(self, data: list, unique_code: str, nom_data = None, is_patch = False):
        for item in data:
            if item.nomenclature.unique_code == unique_code:
                if is_patch:
                    self.set_nom_values(item, nom_data)
                else:
                    return True
        return False
    
    def set_nom_values(self, item, new_item):
        item.nomenclature.name = new_item.name
        item.nomenclature.range = new_item.range
        item.nomenclature.group = new_item.group
        
                    
            
    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        
        if type == event_type.DELETE_NOMENCLATURE:
            return self.delete_nomenclature(params)
        elif type == event_type.CHANGE_NOMENCLATURE:
            return self.patch_nomenclature(params)
    
    
    def set_exception(self, ex: Exception):
        return super().set_exception(ex)